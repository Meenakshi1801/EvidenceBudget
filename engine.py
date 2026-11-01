"""EvidenceBudget 0.1.0: deterministic planning under explicit assumptions."""
import hashlib
import json
from decimal import Decimal, InvalidOperation
from itertools import combinations

VERSION = '0.1.0'
class ValidationError(ValueError):
    pass

def number(v, label, integer=False):
    if isinstance(v, bool) or not isinstance(v, (int,float,str)):
        raise ValidationError(f'{label}: expected a non-negative number')
    try:
        d=Decimal(str(v))
    except InvalidOperation:
        raise ValidationError(f'{label}: invalid number') from None
    if not d.is_finite() or d < 0 or (integer and d != d.to_integral_value()):
        raise ValidationError(f'{label}: expected a finite non-negative '+('integer' if integer else 'number'))
    return d

def fingerprint(checkpoint):
    """Approval binds all checkpoint content, including costs and conditions."""
    payload={k:v for k,v in checkpoint.items() if k!='approval'}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()

def validate(case):
    if not isinstance(case,dict): raise ValidationError('Case must be an object')
    for key in ('case_id','title','assignment','ai_permissions'):
        if not isinstance(case.get(key),str) or not case[key].strip(): raise ValidationError(f'{key}: nonempty text required')
    n=number(case.get('class_size'),'class_size',True)
    if n==0: raise ValidationError('class_size must be positive')
    for key in ('teacher_budget','student_budget','fixed_teacher_setup'):
        number(case.get(key),key)
    req=case.get('requirements')
    if not isinstance(req,list) or not req: raise ValidationError('At least one requirement is required')
    ids=[]
    for r in req:
        if not isinstance(r,dict) or not isinstance(r.get('id'),str) or not r['id']: raise ValidationError('Invalid requirement ID')
        ids.append(r['id'])
        if not isinstance(r.get('description'),str) or not r['description'].strip(): raise ValidationError('Requirement description required')
        k=number(r.get('minimum',1),'minimum',True)
        if k==0: raise ValidationError('Requirement minimum must be positive')
    if len(set(ids))!=len(ids): raise ValidationError('Duplicate requirement ID')
    cps=case.get('checkpoints')
    if not isinstance(cps,list) or not 1<=len(cps)<=12: raise ValidationError('Use 1 to 12 checkpoints for exhaustive enumeration')
    cids=[c.get('id') if isinstance(c,dict) else None for c in cps]
    if any(not isinstance(i,str) or not i for i in cids) or len(set(cids))!=len(cids): raise ValidationError('Invalid or duplicate checkpoint ID')
    for c in cps:
        for field in ('name','prompt','conditions','ai_permissions','mapping_rationale'):
            if not isinstance(c.get(field),str) or not c[field].strip(): raise ValidationError(f'{c["id"]}: {field} required')
        for key in ('preparation','review_per_unit','delivery','student_minutes'):
            number(c.get(key),f'{c["id"]}.{key}')
        units=number(c.get('review_units'),'review_units',True)
        if c.get('review_basis') not in ('student','group'): raise ValidationError('review_basis must be student or group')
        if c['review_basis']=='student' and units!=n: raise ValidationError('Student review units must equal class size; sampling is not supported')
        if c['review_basis']=='group' and (units==0 or units>n): raise ValidationError('Invalid group review count')
        if not isinstance(c.get('available'),bool): raise ValidationError('available must be boolean')
        cov=c.get('coverage')
        if not isinstance(cov,list) or any(i not in ids for i in cov) or len(cov)!=len(set(cov)): raise ValidationError('Unknown or duplicate coverage requirement')
        if cov and c.get('evidence_scope')!='individual_all': raise ValidationError('Mandatory coverage requires individual evidence for all students')
        if c.get('evidence_scope') not in ('individual_all','context_only'): raise ValidationError('Invalid evidence scope')
        for key in ('requires','excludes'):
            refs=c.get(key,[])
            if not isinstance(refs,list) or any(i not in cids or i==c['id'] for i in refs): raise ValidationError(f'Invalid {key} reference')
        try: current=fingerprint(c)
        except (ValueError,TypeError): raise ValidationError('Checkpoint must contain JSON-safe values') from None
        a=c.get('approval',{})
        if cov and (not isinstance(a,dict) or a.get('fingerprint')!=current or not a.get('reviewer') or not a.get('status') in ('development_assumption','teacher_approved')):
            raise ValidationError(f'{c["id"]}: mapping needs approval for its current content')
    # Detect dependency cycles explicitly instead of permitting circular prerequisites.
    graph={c['id']:c.get('requires',[]) for c in cps}
    def visit(i,path,done):
        if i in path: raise ValidationError('Cyclic checkpoint dependency')
        if i in done:return
        for j in graph[i]:visit(j,path|{i},done)
        done.add(i)
    done=set()
    for i in graph:visit(i,set(),done)

def cost(c):
    return number(c['preparation'],'P')+number(c['review_units'],'N',True)*number(c['review_per_unit'],'R')+number(c['delivery'],'L')

def _value(d): return int(d) if d==int(d) else float(d)

def _plan(case, selected):
    teacher=number(case['fixed_teacher_setup'],'setup')+sum((cost(c) for c in selected),Decimal(0))
    student=sum((number(c['student_minutes'],'S') for c in selected),Decimal(0))
    counts={r['id']:sum(r['id'] in c['coverage'] for c in selected) for r in case['requirements']}
    gaps={r['id']:max(0,int(r.get('minimum',1))-counts[r['id']]) for r in case['requirements']}
    return {'selected':[c['id'] for c in selected], 'teacher_minutes':_value(teacher),'student_minutes':_value(student),'coverage_counts':counts,'unmet_requirements':{k:v for k,v in gaps.items() if v},'cost_breakdown':[{'id':c['id'],'teacher_minutes':_value(cost(c))} for c in selected]}

def solve(case):
    validate(case)
    cps=case['checkpoints']; valid=[]
    for size in range(len(cps)+1):
        for subset in combinations(cps,size):
            chosen={c['id'] for c in subset}
            if any(not c['available'] or not set(c.get('requires',[]))<=chosen or set(c.get('excludes',[]))&chosen for c in subset):continue
            valid.append(_plan(case,subset))
    sb=number(case['student_budget'],'student_budget'); tb=number(case['teacher_budget'],'teacher_budget')
    complete=[p for p in valid if not p['unmet_requirements']]
    student_ok=[p for p in complete if number(p['student_minutes'],'S')<=sb]
    feasible=[p for p in student_ok if number(p['teacher_minutes'],'T')<=tb]
    # Coverage counts are capped at the specified thresholds: excess is not assumed to improve evidence quality.
    frontier=[p for p in feasible if not any(q['teacher_minutes']<=p['teacher_minutes'] and q['student_minutes']<=p['student_minutes'] and (q['teacher_minutes']<p['teacher_minutes'] or q['student_minutes']<p['student_minutes']) for q in feasible)]
    frontier.sort(key=lambda p:(p['teacher_minutes'],p['student_minutes'],p['selected']))
    minimum=min((p['teacher_minutes'] for p in student_ok),default=None)
    missing=[r['id'] for r in case['requirements'] if not any(p['coverage_counts'][r['id']]>=int(number(r.get('minimum',1),'minimum',True)) for p in valid)]
    if feasible: reason='feasible'
    elif not complete: reason='evidence_or_structural_gap'
    elif not student_ok: reason='student_budget_exceeded'
    else: reason='teacher_budget_exceeded'
    closest=sorted(valid,key=lambda p:(sum(p['unmet_requirements'].values()),max(0,p['teacher_minutes']-float(tb))+max(0,p['student_minutes']-float(sb)),p['teacher_minutes'],p['selected']))[:5]
    return {'engine_version':VERSION,'case_id':case['case_id'],'case_sha256':hashlib.sha256(json.dumps(case,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest(),'status':reason,'feasible_count':len(feasible),'pareto_plans':frontier,'minimum_teacher_minutes_with_student_limit':minimum,'teacher_shortfall':max(0,minimum-float(tb)) if minimum is not None else None,'requirements_unreachable_in_any_legal_plan':missing,'minimum_student_minutes_without_budgets':min((p['student_minutes'] for p in complete),default=None),'diagnostic_plans':closest if not feasible else [],'unavailable':[c['id'] for c in cps if not c['available']],'warning':'Feasibility uses declared assumptions. It does not establish assessment validity, authorship, or student learning. Multiple demonstrations are counts, not proof of independent evidence.'}
