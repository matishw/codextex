# URL to PDF App

This app lets you submit a URL and downloads a PDF of the full page.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
python app.py
```

Visit `http://localhost:5000` and enter a URL to generate a PDF.
