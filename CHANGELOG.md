# Changelog

## 0.5.9 — unify teacher-facing terminology

- Use teacher, student and generative AI consistently in the interface, PDF blueprint, sample plans and user guides.
- Align time-limit and checkpoint wording across the planning screens and exported blueprint.
- Update the quick-start guides to match the current sample-plan, review and PDF controls.


## 0.5.8 — clarify intended teaching contexts

- State that EvidenceBudget can support school and university assessment planning, with examples and estimates adapted to the local context.


## 0.5.7 — clarify teacher-facing labels and PDF saving

- Replace abbreviations and technical labels with plain-language wording.
- Remove repeated accessibility guidance within each checkpoint and clarify the time estimate help.
- Rename the PDF action to match the browser print/save flow.


## 0.5.6 — highlight the save reminder

- Label the unsaved-work reminder “Important” and set it apart in a soft red notice.
- Clarify that sample plans should be adapted to the teacher’s class.


## 0.5.5 — align the usage guide with the approved wording

- Present the app purpose under “About EvidenceBudget” and the five navigation steps under “Plan your assessment step by step.”


## 0.5.4 — clarify the app purpose

- Add a short plain-language introduction to the usage guide explaining what EvidenceBudget helps teachers do.
- Remove the decorative period after EvidenceBudget in the sidebar wordmark.


## 0.5.3 — clear stale messages when changing pages

- Clear page-specific notices and errors when navigating to another section, so a review reminder does not appear on the welcome page.
- Keep the review checkbox validation on the checkpoint review page.


## 0.5.2 — restore the green sidebar navigation

- Keep the warm gradient for buttons within the workspace.
- Restore the sidebar buttons to green outlined controls with a pale-green active state.


## 0.5.1 — unify buttons and soften workspace styling

- Use the welcome page’s warm yellow-to-peach gradient across interface buttons.
- Add gentle mint, lavender, and peach accents to workspace panels, checkpoint cards, hints, and page backgrounds while keeping entry fields white for readability.


## 0.5.0 — add colorful creator welcome page

- Highlight the app descriptor and redesign the opening page with a colorful two-column portrait and creator profile.
- Show the creator’s name, role, School of Education, and university affiliation without a department listing.
- Serve the profile photo within the local app and include the same updated credit near the top of PDF blueprints.


## 0.4.9 — add welcome cover and move creator credit

- Add a welcome page with the app title, purpose, and developer affiliation before the usage guide.
- Add a “Get started” button to open the “How to use EvidenceBudget” guide.
- Move the creator credit from the repeating footer to the welcome page; keep it near the top of the PDF blueprint.


## 0.4.8 — add creator and affiliation credit

- Show the concept and development credit in the teacher interface and PDF blueprint.
- Align the app, sidebar, and README release labels at 0.4.8.


## 0.4.7 — simplify sample controls

- Remove the redundant “TRY A SAMPLE PLAN” sidebar heading; the sample selector label and action button remain.


## 0.4.6 — clear next-step navigation

- Add a bottom “Next: checkpoints & review” button to the evidence requirements page, with a back button to assignment.
- Clarify that confirming the checkpoint review proceeds to plan comparison.
- Keep the top “Compare plans” control on the comparison page only.


## 0.4.5 — keep start-page message on the start page

- Clear ordinary welcome and status messages when moving into a workspace step, so the orange strip does not repeat the start-page instruction on every page.
- Keep error messages visible until the user can act on them.


## 0.4.4 — simpler sample-plan language

- Replace “worked example” wording on the guided start with “sample plan” language.
- Use the short message “This is a sample. Make it your own.” after opening a sample.
- Explain in plain language that teachers can change the sample to fit their class.


## 0.4.3 — guided start and blank workspace

- Open the app on a concise instructional page instead of preloading the worked case into the assignment fields.
- Add a clear “Start a blank assignment” action; begin with empty assignment, evidence, checkpoint, and budget fields.
- Keep the worked case available as an explicit optional example.

## 0.4.2 — PDF page-break refinement

- Allow long checkpoint details to flow across pages instead of moving the entire section to a new page and leaving a large blank area.
- Keep section headings with their following content to reduce orphan headings.
- Based on inspection of a representative teacher-exported blueprint; re-export once on this build to confirm the layout in the Codespaces browser.

## 0.4.1 — expert-review usability fixes

- Move directly to plan comparison after a successful review confirmation.
- Add a server version check and plain Codespaces restart guidance when the preview is connected to an older server.
- Add a checkpoint field for an alternative response/accessibility route with an adjacent reminder to judge evidence equivalence.
- Allow long unbroken text to wrap in the readable PDF print layout.
- Expert-review findings EX5–EX7 informed these changes; the revised build still needs follow-up review and PDF inspection.

## 0.4.0 — teacher-readable PDF record

- Replaced visible JSON export/import controls with a readable print-to-PDF blueprint containing assignment context, evidence requirements, selected checkpoint details, time assumptions, and the review record.
- Kept machine-readable JSON out of the teacher-facing interface.

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
