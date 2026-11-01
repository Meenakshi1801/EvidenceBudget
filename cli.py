"""Run: python cli.py examples/case_01.json --output result.json"""
import argparse
import json
import sys
from pathlib import Path
from engine import solve, ValidationError

def main():
    p=argparse.ArgumentParser(description='EvidenceBudget planning engine')
    p.add_argument('case',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        case=json.loads(a.case.read_text(encoding='utf-8')); result=solve(case)
        data=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n'
        if a.output:a.output.write_text(data,encoding='utf-8')
        print(f"{result['case_id']}: {result['status']}; feasible combinations: {result['feasible_count']}")
        for plan in result['pareto_plans']:
            print(f"  {' + '.join(plan['selected'])}: teacher {plan['teacher_minutes']} min; student {plan['student_minutes']} min")
        if not a.output:print(data)
        return 0
    except (ValidationError,ValueError,OSError,TypeError,KeyError) as e:
        print(f'Error: {e}',file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
