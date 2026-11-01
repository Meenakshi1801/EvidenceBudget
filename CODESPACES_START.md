# Run EvidenceBudget in Codespaces

Open the repository Codespace on branch `main`. In a terminal at the repository root, update the workspace:

```sh
git pull --ff-only origin main
```

If an older app is running, click the terminal whose output says **EvidenceBudget teacher interface** and press **Ctrl+C** once. Do not delete the terminal. Start the updated app in that terminal:

```sh
python3 app.py --host 0.0.0.0 --no-browser
```

Keep that terminal open. Open the **Ports** panel, find port **8765**, and choose **Open in Browser**. Keep port visibility Private during development. This preview works only while the Codespace is running; it is not permanent hosting.

The app checks that the browser page and server use the same release. If it reports a version mismatch, stop the old server in its terminal, pull the latest `main` changes, restart the app, then reopen port 8765.

Teacher entries are not saved automatically. Compare plans and create a readable PDF record before closing. The teacher interface does not offer JSON downloads. This local development server is for review, not production hosting.
