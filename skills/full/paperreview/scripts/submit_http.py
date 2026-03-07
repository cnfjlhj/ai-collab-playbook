from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

BASE_URL = "https://paperreview.ai"
DEFAULT_EMAIL = ""
DEFAULT_TOKEN_FILENAME_SUFFIX = ".paperreview.token.txt"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="paperreview-submit",
        description=(
            "Submit a PDF to paperreview.ai using their public endpoints "
            "(get presigned URL -> upload to S3 -> confirm upload). "
            "Provide your own email via --email when submitting."
        ),
    )
    parser.add_argument("--pdf", required=True, help="Path to a local PDF file")
    parser.add_argument(
        "--venue",
        default="ICLR",
        help="Target venue value (default: ICLR). Use 'Other' with --custom-venue.",
    )
    parser.add_argument(
        "--custom-venue",
        default="",
        help="Custom venue text (only used when --venue Other).",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not perform any network calls; only validate inputs (recommended first).",
    )
    mode.add_argument(
        "--submit",
        action="store_true",
        help="Perform the real submission (network + S3 upload).",
    )
    parser.add_argument(
        "--email",
        default="",
        help="Email used for the paperreview.ai submission. Required with --submit.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="HTTP timeout seconds per request (default: 60).",
    )
    parser.add_argument(
        "--token-file",
        default="",
        help=(
            "Write the returned token to this path after a successful submit. "
            "If omitted, defaults to <pdf>.paperreview.token.txt (next to the PDF)."
        ),
    )
    parser.add_argument(
        "--no-token-file",
        action="store_true",
        help="Do not write any token file even after a successful submit.",
    )
    return parser.parse_args(argv)


def is_pdf_file(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            header = f.read(8)
    except OSError:
        return False
    return header.startswith(b"%PDF-")


def validate_inputs(pdf_path: Path, venue: str, custom_venue: str) -> None:
    if not pdf_path.exists():
        raise ValueError(f"PDF not found: {pdf_path}")
    if not pdf_path.is_file():
        raise ValueError(f"Not a file: {pdf_path}")
    if not is_pdf_file(pdf_path):
        raise ValueError("File does not look like a PDF (missing %PDF- header).")

    size_bytes = pdf_path.stat().st_size
    # The UI currently displays "Max 10MB". Keep this as a warning, not a hard error.
    if size_bytes > 10 * 1024 * 1024:
        print(
            f"WARN: PDF is {size_bytes} bytes (>10MB). The website UI may reject it.",
            file=sys.stderr,
        )

    if venue == "Other" and not custom_venue.strip():
        raise ValueError("--venue Other requires --custom-venue")


def venue_value(venue: str, custom_venue: str) -> str:
    if venue == "Other":
        return custom_venue.strip()
    return venue.strip()


def submit_pdf(pdf_path: Path, venue: str, custom_venue: str, email: str, timeout: float) -> dict:
    selected_venue = venue_value(venue, custom_venue)

    # Step 1: get presigned URL + fields
    get_url = f"{BASE_URL}/api/get-upload-url"
    get_payload = {"filename": pdf_path.name, "venue": selected_venue or ""}
    print("POST", get_url)
    get_resp = requests.post(get_url, json=get_payload, timeout=timeout)
    if get_resp.status_code == 429:
        raise RuntimeError(f"Rate limited (429) on get-upload-url: {get_resp.text}")
    if not get_resp.ok:
        raise RuntimeError(
            f"get-upload-url failed ({get_resp.status_code}): {get_resp.text}"
        )

    get_data = get_resp.json()
    required_keys = ["success", "presigned_url", "s3_key", "presigned_fields"]
    missing = [k for k in required_keys if k not in get_data]
    if missing:
        raise RuntimeError(
            "Invalid get-upload-url response, missing keys: "
            + ", ".join(missing)
            + "\n"
            + json.dumps(get_data, indent=2)[:2000]
        )
    if not get_data.get("success"):
        raise RuntimeError(
            "Server returned success=false:\n" + json.dumps(get_data, indent=2)[:2000]
        )

    presigned_url: str = get_data["presigned_url"]
    s3_key: str = get_data["s3_key"]
    presigned_fields: dict[str, str] = get_data["presigned_fields"]

    # Step 2: upload to S3 via presigned POST
    print("POST", presigned_url)
    with pdf_path.open("rb") as f:
        files = {"file": (pdf_path.name, f, "application/pdf")}
        s3_resp = requests.post(
            presigned_url, data=presigned_fields, files=files, timeout=timeout
        )
    if not s3_resp.ok:
        raise RuntimeError(
            f"S3 upload failed ({s3_resp.status_code}): {s3_resp.text[:2000]}"
        )

    # Step 3: confirm upload (this triggers processing + token)
    confirm_url = f"{BASE_URL}/api/confirm-upload"
    print("POST", confirm_url)
    confirm_form = {"s3_key": s3_key, "venue": selected_venue or "", "email": email}
    confirm_resp = requests.post(confirm_url, data=confirm_form, timeout=timeout)
    if confirm_resp.status_code == 429:
        raise RuntimeError(f"Rate limited (429) on confirm-upload: {confirm_resp.text}")
    if not confirm_resp.ok:
        raise RuntimeError(
            f"confirm-upload failed ({confirm_resp.status_code}): {confirm_resp.text}"
        )

    return confirm_resp.json()


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    pdf_path = Path(args.pdf)

    try:
        validate_inputs(pdf_path, args.venue, args.custom_venue)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    selected_venue = venue_value(args.venue, args.custom_venue)
    print("pdf:", str(pdf_path))
    print("email:", args.email.strip() or "(required for --submit)")
    print("venue:", selected_venue or "(empty)")

    if args.submit and not args.email.strip():
        print("ERROR: --submit requires --email", file=sys.stderr)
        return 2

    if not args.submit:
        # Default safe behavior: avoid accidental submissions.
        print("mode: dry-run (no network calls)")
        print("next: re-run with --submit to perform the real submission")
        return 0

    try:
        result = submit_pdf(pdf_path, args.venue, args.custom_venue, args.email.strip(), args.timeout)
    except Exception as e:
        print(f"ERROR: submit failed: {e}", file=sys.stderr)
        return 1

    print("response:")
    print(json.dumps(result, indent=2)[:3000])
    token = result.get("token")
    if token:
        print("token:", token)

        if not args.no_token_file:
            token_path = (
                Path(args.token_file)
                if args.token_file.strip()
                else pdf_path.with_name(pdf_path.name + DEFAULT_TOKEN_FILENAME_SUFFIX)
            )
            token_path.write_text(f"{token}\n", encoding="utf-8")
            print("token_file:", str(token_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
