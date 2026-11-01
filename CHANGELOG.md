# Changelog
## 0.3.2 — review confirmation enforcement

- Require a recorded overall design review before comparing assessment plans.
- Detect an outdated server response that omits the review record instead of treating confirmation as successful.

## 0.3.1 — review record exports

- Include the reviewer identifier, UTC confirmation time, and reviewed-design fingerprint in assignment, run, and blueprint exports.


## 0.3.0 — reviewer-informed interface revision

- Added an assignment-level learner/classroom context field.
- Clarified that teachers author GenAI permissions at assignment and checkpoint level.
- Added a plain-language evidence glossary and clearer observable-performance examples.
- Clarified one-off setup, cohort preparation/delivery, per-unit review, and per-student workload definitions.
- Exposed preparation, review, delivery, and fixed setup costs in comparison results.
- Improved display of unavailable checkpoints, exclusions, unmet evidence, and teacher/student budget overruns.
- Made explicit that budget changes do not modify evidence requirements.
- Added cautious guidance for accessible response formats and an example with oral and written routes.
- Added `REVIEW_RESPONSE_AND_CHANGELOG.md` with implemented and deferred recommendations.
- Corrected the misleading response-sheet column headings. No review or pilot response values were changed.

Low/typical/high time-range planning is deferred because the current solver uses point estimates. Keyboard, contrast, narrow-screen, and assistive-technology checks remain open and are not claimed as complete.

## 0.2.0 — component cost output

- Added component-level cost breakdowns to planner results while preserving the existing point-estimate calculations.
