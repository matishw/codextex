from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

from flask import Flask, Response, render_template, request, send_file
from playwright.sync_api import sync_playwright

app = Flask(__name__)


def _is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.post("/pdf")
def create_pdf() -> Response:
    url = request.form.get("url", "").strip()
    if not _is_valid_url(url):
        return render_template(
            "index.html",
            error="Please provide a valid http(s) URL.",
            url=url,
        ), 400

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.emulate_media(media="screen")

        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf_path = Path(tmp_file.name)
            page.pdf(path=str(pdf_path), print_background=True, format="A4")

        browser.close()

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="page.pdf",
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
