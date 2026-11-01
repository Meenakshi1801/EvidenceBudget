import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import solve,validate,cost,fingerprint,ValidationError
ROOT=Path(__file__).resolve().parents[1]
def load(i):return json.loads((ROOT/'examples'/f'case_{i:02}.json').read_text())
def approve(c):c['approval']={'status':'development_assumption','reviewer':'test fixture','fingerprint':fingerprint(c)}
class EngineTests(unittest.TestCase):
 def test_six_reference_minima(self):
  for i,v in enumerate([160,110,None,78,131,140],1):
   with self.subTest(case=i):self.assertEqual(solve(load(i))['minimum_teacher_minutes_with_student_limit'],v)
 def test_six_feasible_counts(self):
  self.assertEqual([solve(load(i))['feasible_count'] for i in range(1,7)],[2,0,0,3,4,1])
 def test_budget_boundary(self):
  c=load(1);c['teacher_budget']=160;self.assertEqual(solve(c)['status'],'feasible');c['teacher_budget']=159;self.assertEqual(solve(c)['teacher_shortfall'],1)
 def test_teacher_shortfall(self):
  r=solve(load(2));self.assertEqual(r['status'],'teacher_budget_exceeded');self.assertEqual(r['teacher_shortfall'],10)
 def test_budget_repair(self):
  c=load(2);c['teacher_budget']=110;self.assertEqual(solve(c)['pareto_plans'][0]['selected'],['D'])
 def test_uncovered_requirement(self):self.assertEqual(solve(load(3))['requirements_unreachable_in_any_legal_plan'],['E3'])
 def test_missing_evidence_not_repaired_by_money(self):
  c=load(3);c['teacher_budget']=10000;self.assertEqual(solve(c)['status'],'evidence_or_structural_gap')
 def test_missing_evidence_repair(self):
  c=load(3);g=copy.deepcopy(c['checkpoints'][0]);g.update(id='G',name='Second-source verification',coverage=['E3'],preparation=15,review_per_unit=2,delivery=20,student_minutes=20);approve(g);c['checkpoints'].append(g);self.assertEqual(solve(c)['minimum_teacher_minutes_with_student_limit'],170)
 def test_unavailable_filtered(self):
  r=solve(load(4));self.assertEqual(r['unavailable'],['A']);self.assertEqual([p['selected'] for p in r['pareto_plans']],[['B']])
 def test_exclusion_when_oral_available(self):
  c=load(4);a=c['checkpoints'][0];a['available']=True;approve(a);r=solve(c)
  self.assertTrue(all(not {'A','B'}<=set(p['selected']) for p in r['pareto_plans']))
 def test_group_cost(self):self.assertEqual(cost(load(5)['checkpoints'][0]),51)
 def test_live_cost_counted_once(self):self.assertEqual(cost(load(5)['checkpoints'][2]),130)
 def test_pareto_tradeoff(self):self.assertEqual([p['selected'] for p in solve(load(5))['pareto_plans']],[['B'],['D']])
 def test_dependency_enforced(self):self.assertEqual(solve(load(6))['pareto_plans'][0]['selected'],['A','B','E'])
 def test_unavailable_dependency(self):
  c=load(6);c['checkpoints'][0]['available']=False;self.assertEqual(solve(c)['status'],'evidence_or_structural_gap');self.assertIn('E1',solve(c)['requirements_unreachable_in_any_legal_plan'])
 def test_student_budget_reason(self):
  c=load(1);c['student_budget']=0;self.assertEqual(solve(c)['status'],'student_budget_exceeded')
 def test_fixed_setup(self):
  c=load(1);c['fixed_teacher_setup']=30;self.assertEqual(solve(c)['minimum_teacher_minutes_with_student_limit'],190)
 def test_export_replay(self):
  c=load(6);self.assertEqual(solve(c),solve(json.loads(json.dumps(c))))
 def test_approval_invalidated_by_edit(self):
  c=load(1);c['checkpoints'][0]['prompt']='New task';self.assertRaises(ValidationError,solve,c)
 def test_duplicate_id_rejected(self):
  c=load(1);c['checkpoints'][1]['id']='A';self.assertRaises(ValidationError,solve,c)
 def test_unknown_requirement_rejected(self):
  c=load(1);c['checkpoints'][0]['coverage']=['unknown'];self.assertRaises(ValidationError,solve,c)
 def test_negative_nan_and_boolean_rejected(self):
  for val in [-1,float('nan'),float('inf'),True]:
   c=load(1);c['teacher_budget']=val
   with self.subTest(value=val):self.assertRaises(ValidationError,solve,c)
 def test_group_evidence_cannot_cover_individual(self):
  c=load(5);cp=c['checkpoints'][0];cp['coverage']=['E1'];approve(cp);self.assertRaises(ValidationError,solve,c)
 def test_unknown_dependency_rejected(self):
  c=load(6);c['checkpoints'][1]['requires']=['Z'];self.assertRaises(ValidationError,solve,c)
 def test_cycle_rejected(self):
  c=load(6);c['checkpoints'][0]['requires']=['B'];approve(c['checkpoints'][0]);self.assertRaises(ValidationError,solve,c)
 def test_two_demonstrations(self):
  c=load(1);c['requirements'][0]['minimum']=2;c['teacher_budget']=1000;c['student_budget']=100;r=solve(c);self.assertTrue(r['pareto_plans']);self.assertTrue(all(p['coverage_counts']['E1']>=2 for p in r['pareto_plans']))
 def test_candidate_limit(self):
  c=load(1);c['checkpoints']=c['checkpoints']*3;self.assertRaises(ValidationError,solve,c)
if __name__=='__main__':unittest.main()
