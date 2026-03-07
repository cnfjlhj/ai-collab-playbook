#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SEGMENT_TS_LINE_RE = re.compile(r"^\s*时间戳范围:\s*\[[^\]]+\]\s*$")
BARE_TS_LINE_RE = re.compile(r"^\s*\d{1,2}:\d{2}(?::\d{2})?\s*$")
BOLD_TITLE_LINE_RE = re.compile(r"^\s*\*\*.+\*\*\s*$")


@dataclass(frozen=True)
class Segment:
    start_line: int
    timestamp_line: str
    title_line: str
    body: str


def _split_paragraphs(markdown: str) -> list[str]:
    # Preserve order; collapse multiple blank lines to paragraph boundaries.
    text = markdown.replace("\r\n", "\n")
    paras: list[str] = []
    buf: list[str] = []
    for line in text.split("\n"):
        if line.strip() == "":
            if buf:
                paras.append("\n".join(buf).strip())
                buf = []
            continue
        buf.append(line.rstrip())
    if buf:
        paras.append("\n".join(buf).strip())
    return [p for p in paras if p.strip()]


def parse_segments(lines: list[str]) -> list[Segment]:
    segments: list[Segment] = []
    idx = 0
    n = len(lines)
    while idx < n:
        if not SEGMENT_TS_LINE_RE.match(lines[idx]):
            idx += 1
            continue

        ts_line_no = idx + 1
        ts_line = lines[idx].strip()
        idx += 1

        while idx < n and lines[idx].strip() == "":
            idx += 1
        if idx >= n:
            raise ValueError(f"Line {ts_line_no}: time range found, but title line is missing.")

        title_line_no = idx + 1
        title_line = lines[idx].strip()
        idx += 1

        body_lines: list[str] = []
        while idx < n and not SEGMENT_TS_LINE_RE.match(lines[idx]):
            body_lines.append(lines[idx].rstrip("\n"))
            idx += 1

        body = "\n".join(body_lines).strip()
        segments.append(
            Segment(
                start_line=ts_line_no,
                timestamp_line=ts_line,
                title_line=title_line,
                body=body,
            )
        )

        _ = title_line_no  # for debugging / future extension

    return segments


def validate(text: str) -> list[str]:
    errors: list[str] = []
    lines = text.replace("\r\n", "\n").split("\n")

    segments = parse_segments(lines)
    if not segments:
        errors.append("No segments found. Expected lines like: 时间戳范围: [00:00 - 01:23]")
        return errors

    for seg in segments:
        if not BOLD_TITLE_LINE_RE.match(seg.title_line):
            errors.append(
                f"Line {seg.start_line + 1}: segment title must be Markdown bold (e.g. **标题**). "
                f"Got: {seg.title_line!r}"
            )

        if not seg.body.strip():
            errors.append(f"Line {seg.start_line}: segment body is empty.")
            continue

        # Forbid raw transcript timestamp lines (user requirement: do not include original timestamped material).
        for offset, raw in enumerate(seg.body.split("\n"), start=1):
            if BARE_TS_LINE_RE.match(raw) and not raw.strip().startswith("时间戳范围:"):
                errors.append(
                    f"Line {seg.start_line + 1 + offset}: looks like a raw timestamp line {raw!r}. "
                    "Do not include original line-by-line subtitles in the summary/PDF."
                )

        paras = _split_paragraphs(seg.body)
        mentor_para_idx = None
        for i, p in enumerate(paras):
            if p.lstrip().startswith("【导师评注】"):
                mentor_para_idx = i
                break

        if mentor_para_idx is None:
            errors.append(
                f"Line {seg.start_line}: missing mentor paragraph. Add a new paragraph that starts with '【导师评注】'."
            )
            continue

        if mentor_para_idx == 0:
            errors.append(
                f"Line {seg.start_line}: mentor paragraph appears before the creator summary. "
                "Write the first-person creator summary first, then start a new paragraph with '【导师评注】'."
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate timestamped video summary Markdown format.")
    parser.add_argument("input", type=Path, help="Path to the summary Markdown file (output.md).")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"[ERROR] File not found: {args.input}", file=sys.stderr)
        return 2
    text = args.input.read_text(encoding="utf-8")

    errors = validate(text)
    if errors:
        print("[FAIL] Summary format validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("[OK] Summary format looks good.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

