#!/usr/bin/env python3
"""Extract numbered text pages from a local textbook PDF for review."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pdfplumber


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    pdf_path = args.pdf.resolve()
    if not pdf_path.is_file():
        parser.error(f"PDF not found: {pdf_path}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    digest = hashlib.sha256()
    with pdf_path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)

    pages_path = args.output_dir / "pages.jsonl"
    empty_pages: list[int] = []
    with pdfplumber.open(pdf_path) as pdf, pages_path.open("w", encoding="utf-8", newline="\n") as output:
        page_count = len(pdf.pages)
        for number, page in enumerate(pdf.pages, start=1):
            content = page.extract_text() or ""
            if not content.strip():
                empty_pages.append(number)
            output.write(json.dumps({"pdf_page": f"P{number}", "text": content}, ensure_ascii=False) + "\n")

    report = {
        "source_pdf": str(pdf_path),
        "sha256": digest.hexdigest(),
        "pdf_pages": page_count,
        "empty_text_pages": empty_pages,
        "note": "Text extraction is not a visual or semantic verification.",
    }
    (args.output_dir / "source_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Extracted {page_count} PDF pages to {pages_path}")
    if empty_pages:
        print(f"Pages requiring visual/OCR review: {empty_pages}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
