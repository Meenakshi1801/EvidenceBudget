# EvidenceBudget

Interface version 0.5.9; planning engine version 0.2.0.

EvidenceBudget is an open-source decision-support tool for evidence-centered assessment design. It compares checkpoint combinations against declared evidence requirements, teacher time, student workload, availability, prerequisites, and exclusions. Teachers set any generative-AI rules for their activities. The app does not determine assessment validity, learning, authorship, or whether alternative response formats are equivalent.

## Run locally

Requires Python 3.10 or newer and a modern browser. Runtime uses the Python standard library only.

```sh
python app.py
# Or use the command-line planner:
python cli.py examples/case_01.json --output result.json
```

On Windows, use `py` instead of `python` if needed. Open the local address printed by the app. See [START_HERE.txt](START_HERE.txt) and [USER_GUIDE.md](USER_GUIDE.md) for instructions.

## Included files

- `app.py`, `interface.html`: local browser interface and request handler.
- `engine.py`, `cli.py`: planning engine and command-line entry point.
- `examples/`: synthetic input cases for exploring planner behavior.
- `tests/`: automated software checks.
- `example_result.json`: sample output from a synthetic input.
- `LICENSE`: MIT License.

The included cases are synthetic software fixtures. They do not contain participant records or findings from a study.

## Planning assumptions

Teacher cost combines fixed setup, cohort preparation, per-unit review, and cohort delivery/facilitation. Student cost is active minutes per student. The engine uses single point estimates, enumerates available checkpoint combinations, applies prerequisites and exclusions, and reports feasible plans and diagnostic alternatives. A feasible plan indicates only that entered requirements and time limits are met under the supplied assumptions.

The teacher interface can create a readable PDF blueprint through the browser’s print dialog. Work is not saved automatically. The command-line workflow can read and write JSON.

## Limitations

The software does not validate assessment quality, establish student learning or authorship, authenticate approvals, or determine equivalence between response formats. Review cost estimates, evidence mappings, and local suitability require professional judgment.
