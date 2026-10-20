#!/usr/bin/env python3
"""Validate chapter JSONL structure and merge, without claiming semantic review."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pdfplumber


FIELDS = (
    "knowledge_point_id",
    "chapter",
    "section",
    "knowledge_point",
    "detail",
    "example",
    "pdf_page",
)
PAGE_RE = re.compile(r"^P(\d+)(?:-P(\d+))?$")


def validate_rows(input_dir: Path, pdf_pages: int) -> tuple[list[dict], dict]:
    files = sorted(input_dir.glob("chapter-??-core.jsonl"))
    if not files:
        raise ValueError(f"No chapter-XX-core.jsonl files in {input_dir}")
    rows: list[dict] = []
    errors: list[str] = []
    counts: dict[str, int] = {}
    seen_ids: set[str] = set()
    for file in files:
        previous_page = 0
        count = 0
        chapter_number = int(file.stem.split("-")[1])
        for line_number, line in enumerate(file.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            location = f"{file.name}:{line_number}"
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{location}: invalid JSON: {exc.msg}")
                continue
            if not isinstance(row, dict) or tuple(row) != FIELDS:
                errors.append(f"{location}: expected fields in order {FIELDS}")
                continue
            for field in FIELDS:
                if not isinstance(row[field], str):
                    errors.append(f"{location}: {field} must be a string")
            for field in FIELDS:
                if field != "example" and not str(row[field]).strip():
                    errors.append(f"{location}: {field} is blank")
            identifier = row["knowledge_point_id"]
            count += 1
            id_match = re.fullmatch(r".+-(?:C)?(\d+)-(\d{3})", identifier)
            # Original-text revisions may retain IDs after records are removed or
            # split. IDs must remain unique and chapter-scoped, not renumbered to
            # match a new row position; source mappings carry revision lineage.
            if not id_match or int(id_match.group(1)) != chapter_number:
                errors.append(f"{location}: ID does not match chapter: {identifier}")
            if identifier in seen_ids:
                errors.append(f"{location}: duplicate ID {identifier}")
            seen_ids.add(identifier)
            pages = [PAGE_RE.fullmatch(part.strip()) for part in re.split(r"[；;]", row["pdf_page"])]
            if not pages or any(page is None for page in pages):
                errors.append(f"{location}: invalid PDF page {row['pdf_page']}")
            else:
                start = int(pages[0].group(1))
                previous_end = 0
                for page in pages:
                    segment_start = int(page.group(1))
                    end = int(page.group(2) or segment_start)
                    if not 1 <= segment_start <= end <= pdf_pages:
                        errors.append(f"{location}: page outside PDF: {row['pdf_page']}")
                    if segment_start <= previous_end:
                        errors.append(f"{location}: page segments overlap or move backwards: {row['pdf_page']}")
                    previous_end = end
                if start < previous_page:
                    errors.append(f"{location}: page order moved backwards: {row['pdf_page']}")
                previous_page = start
            rows.append(row)
        counts[file.name] = count
    report = {
        "chapter_counts": counts,
        "total_rows": len(rows),
        "unique_ids": len(seen_ids),
        "pdf_pages": pdf_pages,
        "structural_errors": errors,
        "semantic_review": "not_assessed_by_script",
    }
    return rows, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--input-dir", type=Path, required=True)
    args = parser.parse_args()
    if not args.pdf.is_file():
        parser.error(f"PDF not found: {args.pdf}")
    with pdfplumber.open(args.pdf) as pdf:
        page_count = len(pdf.pages)
    rows, report = validate_rows(args.input_dir, page_count)
    report_path = args.input_dir / "review_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["structural_errors"]:
        print(f"Found {len(report['structural_errors'])} structural errors; see {report_path}")
        return 1
    merged = args.input_dir / "knowledge_points_core.jsonl"
    merged.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8"
    )
    print(f"Merged {len(rows)} rows into {merged}; semantic source review is still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
