# EvidenceBudget teacher quick guide

Interface version 0.5.9; planning engine version 0.2.0 — development build, 1 November 2026

EvidenceBudget is a planning tool for teachers in school and university settings. It helps connect what students should demonstrate to assessment activities, compare estimated teacher and student time, and create a readable PDF blueprint. Teachers set the rules for generative AI use. The app does not judge assessment quality, student learning, or whether alternative response formats are equivalent.

## Start the app in Codespaces

1. In the repository, open **Terminal → New Terminal** and run:
   `git pull --ff-only origin main`
2. If EvidenceBudget is already running, click the terminal whose output says **EvidenceBudget teacher interface** and press **Ctrl+C** once. Do not delete the terminal.
3. Start the updated app:
   `python3 app.py --host 0.0.0.0 --no-browser`
4. Open the **Ports** panel, find port **8765**, and choose **Open in Browser**. If the preview reports a version mismatch, stop the old server and reopen the forwarded port after starting the updated app.

Keep the terminal and Codespace open while using the preview. This is a development preview, not permanent hosting.

## Plan and compare

1. Open **How to use EvidenceBudget**. Choose **Start a blank assignment** to create your own plan, or select a sample in the sidebar and choose **Use a sample plan**.
2. Describe the assignment, what students must produce, the classroom context, and what students may do with generative AI.
3. List the evidence requirements, then add checkpoints and link each checkpoint to the evidence it can show.
4. Enter realistic teacher and student time estimates. For an alternative response format, explain it under **Alternative response or accessibility option** and decide whether it shows the same learning under equivalent criteria.
5. Review the design, enter the teacher name or identifier, and tick the confirmation box. Choose **Confirm review & compare plans**. Any later edit requires a new review.

## Create a PDF record

On the comparison page, choose **Create a readable PDF blueprint** for a plan, then choose **Save as PDF** in the browser print window. The PDF includes the assignment, evidence requirements, selected checkpoint details, planning assumptions and review record.

The teacher interface does not offer JSON downloads. Work is not saved automatically, so create a PDF record before closing. The PDF records the selected plan and assumptions; it is not a validated assessment instrument.

