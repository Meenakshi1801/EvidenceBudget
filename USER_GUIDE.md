# EvidenceBudget teacher quick guide

Interface version 0.4.1; planning engine version 0.2.0 — development build, 1 November 2026

EvidenceBudget helps teachers describe learning evidence, review assessment checkpoints, compare their time costs, and create a readable PDF record. It does not judge educational quality, validate an assessment, or determine whether an accessible response is equivalent.

## Start the app in Codespaces

1. In the repository, open **Terminal → New Terminal** and run:
   `git pull --ff-only origin main`
2. If EvidenceBudget is already running, click the terminal whose output says **EvidenceBudget teacher interface** and press **Ctrl+C** once. Do not delete the terminal.
3. Start the updated app:
   `python3 app.py --host 0.0.0.0 --no-browser`
4. Open the **Ports** panel, find port **8765**, and choose **Open in Browser**. The preview must be on the same release as the running server. If not, the app will display a version-mismatch message.

Keep the terminal and Codespace open while using the preview. The app is a development preview, not permanent hosting.

## Review and compare

1. Enter or edit the assignment, evidence requirements and checkpoint details.
2. For an alternative response format, describe it in **Alternative response/accessibility route (if used)**. Judge whether it elicits the same intended evidence, and apply equivalent criteria. The app cannot certify equivalence.
3. Review the current design assumptions, enter your reviewer name or identifier, and tick the confirmation box.
4. Select **Confirm review**. The app should proceed to the comparison step and calculate available plans. Any later edit requires a new review.

## Create a PDF record

On the comparison page, choose **Download readable PDF blueprint** for a plan. In the browser print window, choose **Save as PDF**. The PDF contains the assignment, evidence requirements, selected checkpoint details, planning assumptions and review record. Long text is set to wrap in the print layout.

The teacher interface does not offer JSON downloads. The app does not save work automatically, so create a PDF record before closing. This PDF records the selected plan and assumptions; it is not a validated assessment instrument.

## Research status

The formative expert review and teacher try-out informed earlier development. Version 0.4.1 responds to expert comments about review navigation, accessibility guidance and PDF readability. This revision still needs follow-up expert review and representative PDF inspection. Small formative reviews do not establish validity, effectiveness or broad usability.
