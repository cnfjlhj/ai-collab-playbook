from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


BASE_URL = "https://paperreview.ai"
DEFAULT_TOKEN_FILENAME_SUFFIX = ".paperreview.token.txt"


@dataclass(frozen=True)
class SavePaths:
    json_path: Path
    md_path: Path


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="paperreview-watch",
        description=(
            "Poll paperreview.ai for a completed review using a token. "
            "When the review is ready (HTTP 200), save timestamped artifacts next to the PDF."
        ),
    )
    parser.add_argument(
        "--token",
        default="",
        help="Review access token. If omitted, read from --token-file or <pdf>.paperreview.token.txt.",
    )
    parser.add_argument(
        "--token-file",
        default="",
        help=(
            "Path to a file containing the token. "
            "If omitted, defaults to <pdf>.paperreview.token.txt (next to the PDF)."
        ),
    )
    parser.add_argument(
        "--pdf",
        required=True,
        help="Path to the PDF that was submitted (used to choose output directory).",
    )
    parser.add_argument(
        "--interval-min",
        type=float,
        default=10.0,
        help="Polling interval in minutes (default: 10).",
    )
    parser.add_argument(
        "--max-hours",
        type=float,
        default=48.0,
        help="Stop polling after this many hours (default: 48).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout seconds per request (default: 30).",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Check only once and exit (does not save files unless review is ready).",
    )
    parser.add_argument(
        "--save-intermediate",
        action="store_true",
        help="Also save a timestamped JSON snapshot for non-200 responses (not recommended).",
    )
    return parser.parse_args(argv)


def build_save_paths(pdf_path: Path, stamp: str) -> SavePaths:
    out_dir = pdf_path.parent
    base = pdf_path.name
    # Do not include the token in filenames to reduce accidental leakage via `ls`.
    json_path = out_dir / f"{base}.paperreview.{stamp}.json"
    md_path = out_dir / f"{base}.paperreview.{stamp}.md"
    return SavePaths(json_path=json_path, md_path=md_path)


def to_markdown(review: dict[str, Any]) -> str:
    title = review.get("title") or "(untitled)"
    venue = review.get("venue") or ""
    submission_date = review.get("submission_date") or ""

    lines: list[str] = []
    lines.append(f"# PaperReview.ai Review\n")
    lines.append(f"## Metadata\n")
    lines.append(f"- Retrieved at: `{_now_iso()}`")
    if title:
        lines.append(f"- Title: {title}")
    if venue:
        lines.append(f"- Venue: {venue}")
    if submission_date:
        lines.append(f"- Submission date: {submission_date}")

    # Optional score fields (keep generic)
    for key in ["overall_score", "score", "rating"]:
        if key in review and review.get(key) is not None:
            lines.append(f"- {key}: {review.get(key)}")

    lines.append("")

    sections = review.get("sections") or {}
    if isinstance(sections, dict) and sections:
        def add_section(header: str, content: Any) -> None:
            if content is None:
                return
            text = str(content).strip()
            if not text:
                return
            lines.append(f"## {header}\n")
            lines.append(text)
            lines.append("")

        # Common keys observed in the site JS
        add_section("Summary", sections.get("summary"))
        add_section("Strengths", sections.get("strengths"))
        add_section("Weaknesses", sections.get("weaknesses"))
        add_section("Detailed Comments", sections.get("detailed_comments"))
        add_section("Questions", sections.get("questions"))

        # Any additional sections not covered above
        known = {"summary", "strengths", "weaknesses", "detailed_comments", "questions"}
        for k, v in sections.items():
            if k in known:
                continue
            header = str(k).replace("_", " ").title()
            add_section(header, v)

    else:
        lines.append("## Review\n")
        lines.append("_No sections field found in response._\n")

    return "\n".join(lines).rstrip() + "\n"


def fetch_review(token: str, timeout: float) -> requests.Response:
    url = f"{BASE_URL}/api/review/{token}"
    return requests.get(url, timeout=timeout)


def save_ready(review: dict[str, Any], token: str, pdf_path: Path) -> SavePaths:
    stamp = _now_stamp()
    paths = build_save_paths(pdf_path, stamp)

    payload = dict(review)
    payload["_retrieved_at"] = _now_iso()
    payload["_token"] = token

    paths.json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    paths.md_path.write_text(to_markdown(review), encoding="utf-8")
    return paths


def save_snapshot(data: Any, token: str, pdf_path: Path, status: int | None) -> Path:
    stamp = _now_stamp()
    out_dir = pdf_path.parent
    base = pdf_path.name
    suffix = f"status{status}" if status is not None else "statusNA"
    path = out_dir / f"{base}.paperreview.{stamp}.{suffix}.json"
    payload = {
        "_retrieved_at": _now_iso(),
        "_token": token,
        "_status": status,
        "data": data,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    pdf_path = Path(args.pdf)

    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        return 2
    if not pdf_path.is_file():
        print(f"ERROR: Not a file: {pdf_path}", file=sys.stderr)
        return 2
    token = args.token.strip()
    if not token:
        token_path = (
            Path(args.token_file)
            if args.token_file.strip()
            else pdf_path.with_name(pdf_path.name + DEFAULT_TOKEN_FILENAME_SUFFIX)
        )
        if not token_path.exists():
            print(
                f"ERROR: --token not provided and token file not found: {token_path}",
                file=sys.stderr,
            )
            return 2
        token = token_path.read_text(encoding="utf-8").strip()
        if not token:
            print(f"ERROR: token file is empty: {token_path}", file=sys.stderr)
            return 2

    interval_s = max(5.0, args.interval_min * 60.0)
    deadline = time.time() + max(0.0, args.max_hours) * 3600.0

    print("pdf:", str(pdf_path))
    print("token: (redacted)")
    print("interval_min:", args.interval_min)
    print("max_hours:", args.max_hours)
    print("once:", bool(args.once))

    attempt = 0
    while True:
        attempt += 1
        print(f"[{_now_iso()}] attempt {attempt}: GET /api/review/{{token}}")

        try:
            resp = fetch_review(token, args.timeout)
        except Exception as e:
            print(f"WARN: request failed: {e!r}", file=sys.stderr)
            if args.once:
                return 1
            if time.time() >= deadline:
                print("ERROR: exceeded max-hours while retrying", file=sys.stderr)
                return 1
            time.sleep(interval_s)
            continue

        status = resp.status_code
        try:
            data = resp.json()
        except Exception:
            data = {"raw_text": resp.text[:4000]}

        if status == 200:
            if not isinstance(data, dict):
                print("ERROR: unexpected 200 response format (not a JSON object)", file=sys.stderr)
                if args.save_intermediate:
                    snap = save_snapshot(data, token, pdf_path, status)
                    print("saved snapshot:", str(snap))
                return 1

            paths = save_ready(data, token, pdf_path)
            print("READY: saved", str(paths.json_path))
            print("READY: saved", str(paths.md_path))
            return 0

        # 202 is expected while processing
        detail = None
        if isinstance(data, dict):
            detail = data.get("detail") or data.get("message")
        print(f"status: {status}" + (f" ({detail})" if detail else ""))

        if args.save_intermediate:
            snap = save_snapshot(data, token, pdf_path, status)
            print("saved snapshot:", str(snap))

        if args.once:
            # Not ready yet; keep non-error exit so it can be used in cron.
            return 0

        if time.time() >= deadline:
            print("ERROR: exceeded max-hours without receiving a ready review", file=sys.stderr)
            return 1

        time.sleep(interval_s)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
