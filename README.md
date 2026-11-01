# EvidenceBudget teacher app and planning engine

Interface version 0.4.2; engine version 0.2.0 — development release, 1 November 2026

EvidenceBudget: An Open-Source Decision-Support Tool for Evidence-Centered Assessment Design with Generative AI.

This runnable Python engine compares checkpoint combinations against declared evidence requirements, teacher time and student workload. It includes six illustrative development cases. The browser interface supports assignment context, teacher-authored AI permissions, evidence mapping, review confirmation and plan comparison. Teachers can create a readable PDF record; machine-readable JSON is not exposed as a teacher-facing download. It does not generate AI permissions or infer assessment validity.

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

Teacher cost = fixed one-off setup + sum(preparation for the cohort + review units × review minutes per unit + delivery/facilitation for the cohort). Student cost is the sum of active minutes per student. Live scoring belongs in delivery only; simultaneous classroom attendance is counted once. The engine uses one point estimate per cost and does not model low/typical/high scenarios. Record uncertain assumptions separately and interpret the computed plan using the entered typical values.

The engine enumerates all subsets (maximum 12 candidates), applies availability, prerequisites and exclusions, counts approved requirement mappings, and checks the two budgets. It returns feasible count, non-dominated plans, minimum teacher cost under the student limit, time shortfall, component-level teacher costs, and diagnostic alternatives if no plan is feasible. Diagnostic alternatives identify unmet requirements and budget overruns, and are not feasible recommendations.

Coverage counts are capped conceptually at the required thresholds when comparing complete plans. Additional demonstrations are not assumed to improve evidence quality. Requiring two demonstrations counts two selected checkpoints; the user must separately establish whether they provide sufficiently distinct evidence. Combined structural conflicts may prevent full coverage even when each requirement is individually reachable. Inspect diagnostic plans and dependencies in such cases. There is no minimal-conflict-set or timetable solver in this release.

All mandatory mappings describe individual evidence for every student. Group products and reflections remain context-only unless a properly specified individual demonstration is approved. One selected checkpoint counts at most once toward each linked requirement; duplicate links do not increase a requirement's count. A count of demonstrations does not establish that they are independent or sufficient. Accessible response formats may be considered only when the teacher judges that they elicit the same intended evidence and uses equivalent criteria; the software does not determine equivalence. Sampling, mixed individual accommodation routes, parallel resource scheduling and programme-level optimisation are outside this release.

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

The command-line engine result JSON records engine version, input SHA256, selected identifiers, coverage counts, unmet requirements and a cost breakdown. The teacher interface instead offers a readable blueprint through the browser print dialog: select “Save as PDF.” The PDF includes the selected plan, assignment, evidence, checkpoint details, time assumptions and review record. Machine-readable JSON remains part of developer/command-line workflows and is not offered as a teacher-interface download.

## Research and release limits

No student learning, authorship, misconduct or assessment-validity inference follows from a feasible plan. A formative review with seven experts and a teacher try-out with eight teachers informed version 0.3.0. The 0.4.1 changes respond to recorded expert comments about the confirmation-to-comparison step, accessibility-equivalence guidance and PDF wrapping. This revised build still needs follow-up expert review and PDF inspection; the formative activities do not establish validity, effectiveness, or broad usability. Costs and mappings require local review and pilot calibration. No external API, network access, keys or student records are needed. Optional GenAI assistance is deferred. Before publication, complete the novelty comparison, document ethics and recruitment procedures, consider a post-revision follow-up, and complete journal-specific release checks.

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

Open `START_HERE.txt` for launch instructions. The local app has no persistent data store, account system or external API. Teacher entries are not sent to an external service. The UI and Python server must be used together; opening interface.html directly is unsupported. After comparing plans, choose “Download readable PDF blueprint,” then “Save as PDF” in the browser print dialog. The app does not automatically save drafts.

The UI requires renewed review after any input edit. The review confirmation applies to the current complete design. Example fixtures can be explored under their labelled development assumptions. A successful review now proceeds directly to plan comparison. If the preview reports a server-version mismatch, stop the terminal running the old EvidenceBudget server and start the updated app as described in `CODESPACES_START.md`.

The graphical interface does not implement automatic checkpoint generation or time-range optimisation. To create a new assessment, enter its requirements, add checkpoints, and review each mapping rationale. AI permissions are teacher-authored and must be specified for each task stage. Group units and delivery times require manual recalculation when class size changes. Unavailable checkpoints are excluded; exclusions and prerequisites can make combinations illegal.

Exports of a selected blueprint include inputs, engine result, selected plan and student-facing instructions. Print provides the current comparison view, not a separately formatted publication document. There is no student record collection.

Review-driven changes in version 0.3.0 clarified context, teacher-authored AI rules, independent evidence, cost assumptions, mappings and budget shortfalls. Version 0.4.1 follows recorded expert suggestions with clearer review navigation, an adjacent accessibility-equivalence reminder, a server-version check and long-text PDF wrapping. The app exposes component-level costs and keeps the validity/authorship/learning limitation beside results. Low/typical/high time-range planning and full keyboard, contrast and assistive-technology checks remain to be completed; do not treat the expert review as software accessibility certification.

Additional files: `app.py`, `interface.html`, `START_WINDOWS.bat`, `START_HERE.txt`, `tests/test_app.py`. This is a local Python application package; it has not been deployed to a hosted website or public repository.
