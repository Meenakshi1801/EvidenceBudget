# Run EvidenceBudget in Codespaces

Open a terminal in the repository root and run:

```sh
python app.py --host 0.0.0.0 --no-browser
```

Open the Ports panel, find 8765, and select Open in Browser. Keep port visibility Private during development. The preview works while this Codespace is running; it is not permanent hosting.

Run checks in a separate terminal:

```sh
python -m unittest discover -s tests -v
```

Export assignments before closing the app. There is no automatic save or external AI API. Development examples require expert review. The localhost development server is for preview, not production hosting. See USER_GUIDE.md for details.
