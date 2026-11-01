# EvidenceBudget teacher app and planning engine

Interface version 0.2.0; engine version 0.1.0 — development release, 1 November 2026

EvidenceBudget: An Open-Source Decision-Support Tool for Evidence-Centered Assessment Design with Generative AI.

This runnable Python engine compares checkpoint combinations against declared evidence requirements, teacher time and student workload. It includes all six original development cases. It now includes a local browser interface for entering assignments, editing requirements and checkpoints, confirming review, comparing plans, and exporting assignment inputs or assessment blueprints. Optional AI drafting is not included.

## Quick start

Install Python 3.10 or newer. There are no third-party runtime dependencies. Unzip this package and open a terminal inside its folder. On Windows, use `py` instead of `python` if needed.

```sh
python app.py
# Or use the command-line engine:
python cli.py examples/case_01.json --output my_result.json
python -m unittest discover -s tests -v
```

Case 01 returns E at 160 teacher minutes and 20 student minutes. Other complete combinations remain included in `feasible_count`, while `pareto_plans` removes cost-dominated combinations. No educational-quality ranking is inferred.

## Included cases

| Case | Minimum teacher minutes under student limit | Initial status |
|---|---:|---|
| 01 Lesson planning | 160 | Feasible |
| 02 Research methods | 110 | Teacher budget short by 10 |
| 03 Source critique | None | E3 has no eligible evidence |
| 04 Accessible science reasoning | 78 | Feasible |
| 05 Group project | 131 | Feasible; B and D trade off teacher/student time |
| 06 Human–AI collaboration | 140 | Feasible; B requires A |

These are illustrative development fixtures, not research results. The expanded Case 01 adds two candidates to the protocol's original four-candidate example, changing its minimum from 170 to 160 minutes.

## Logic and interpretation

Teacher cost = fixed setup + sum(preparation + review_units × review_per_unit + delivery). Student cost is the sum of active minutes per student. Live scoring belongs in delivery only; simultaneous classroom attendance is counted once. The engine cannot discover whether you entered double-counted costs: inspect assumptions.

The engine enumerates all subsets (maximum 12 candidates), applies availability, prerequisites and exclusions, counts approved requirement mappings, and checks the two budgets. It returns feasible count, non-dominated plans, minimum teacher cost under the student limit, time shortfall, and diagnostic alternatives if no plan is feasible. Diagnostic plans are explicitly incomplete or over budget and must not be used as feasible recommendations.

Coverage counts are capped conceptually at the required thresholds when comparing complete plans. Additional demonstrations are not assumed to improve evidence quality. Requiring two demonstrations counts two selected checkpoints; the user must separately establish whether they provide sufficiently distinct evidence. Combined structural conflicts may prevent full coverage even when each requirement is individually reachable. Inspect diagnostic plans and dependencies in such cases. There is no minimal-conflict-set or timetable solver in this release.

All mandatory mappings describe individual evidence for every student. Group products and reflections remain context-only unless a properly specified individual demonstration is approved. Sampling, mixed individual accommodation routes, parallel resource scheduling and programme-level optimisation are outside this release.

## Editing and approval

Edit a copy of the JSON case. Each checkpoint records prompt, conditions, AI permissions, evidence links, rationale, costs, availability and dependencies. Every mapped checkpoint requires a content fingerprint and reviewer identity. Editing checkpoint content invalidates that approval and causes a clear validation error. Budget changes do not change checkpoint content.

After reviewing the revised checkpoint, update its approval explicitly in Python:

```python
import json
from engine import fingerprint
case = json.load(open('my_case.json', encoding='utf-8'))
checkpoint = case['checkpoints'][0]
# First inspect the prompt, conditions, permissions, mapping and estimates.
checkpoint['approval'] = {
    'status': 'teacher_approved',
    'reviewer': 'Your reviewer identifier',
    'fingerprint': fingerprint(checkpoint)
}
with open('my_case.json', 'w', encoding='utf-8') as output:
    json.dump(case, output, indent=2, ensure_ascii=False)
```

Fingerprints detect stale approval; they are not digital signatures or identity authentication. The development fixtures use `development_assumption` with expert review explicitly pending. AI never approves mappings. Outcomes and evidence requirements must also be reviewed whenever their meaning changes; the engine does not provide an authenticated review workflow.

## Outputs and reproducibility

The result JSON records engine version, input SHA256, selected identifiers, coverage counts, unmet requirements and a cost breakdown. Retain both the input JSON and result JSON; the result alone cannot reconstruct the input. Rerun the same input on this engine version to reproduce it. Normalise input types if comparing checksums: semantically similar numeric strings and numbers have different input hashes.

## Research and release limits

No student learning, authorship, misconduct or assessment-validity inference follows from a feasible plan. No empirical expert review or teacher evaluation has been completed. Costs and mappings require local review and pilot calibration. No external API, network access, keys or student records are needed. Optional GenAI assistance is deferred. Before publication, complete the novelty comparison, expert review, approved pilot and journal-specific release checks.

## Package

- `engine.py`: validation, approval fingerprints, costs, subset search and explanations.
- `cli.py`: runnable command-line entry point.
- `examples/`: six editable inputs with full development notes.
- `tests/`: reference cases, boundaries, dependencies, invalid inputs and replay.
- `verification.txt`: output of the executed test run.
- `example_result.json`: actual Case 01 output.
- `LICENSE`: MIT licence; review ownership before public distribution.

This package has been prepared for local review. It has not been published to a public repository.

## Teacher interface

Open `START_HERE.txt` for launch instructions. The local app binds only to 127.0.0.1. It has no persistent data store, account system or external API. Export your assignment before closing. Teacher entries are not sent to an external service. The UI and Python server must be used together; opening interface.html directly is unsupported.

The UI requires renewed review after any input edit, including changes to evidence-requirement descriptions. Changing budgets also requires a fresh confirmation in this first implementation. Example fixtures can be explored under their labelled development assumptions. Import validates the current engine schema; incomplete drafts with empty prompts must be completed before they can be reimported. Export completed inputs regularly.

The graphical interface does not implement automatic checkpoint generation. To create a new assessment, enter its requirements, add checkpoints, and review the mappings. Checkpoint conditions and AI permissions must be inspected at activity level. Group units and delivery times require manual recalculation when class size changes.

Exports of a selected blueprint include inputs, engine result, selected plan and student-facing instructions. Print provides the current comparison view, not a separately formatted publication document. There is no student record collection.

Verification: 36 automated engine and HTTP checks pass. The JavaScript passes Node syntax checking. Interactive visual, keyboard and assistive-technology testing has not been completed; do not treat these checks as classroom usability or accessibility validation.

Additional files: `app.py`, `interface.html`, `START_WINDOWS.bat`, `START_HERE.txt`, `tests/test_app.py`. This is a local Python application package; it has not been deployed to a hosted website or public repository.
