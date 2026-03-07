---
name: paperreview
description: Use when the user explicitly wants to upload a final or near-final PDF to paperreview.ai for an external second opinion. Skip this for local paper critique, which should go through `paper-review-pipeline` first.
version: 0.1.0
---

# paperreview.ai submission

## Purpose

Submit a paper PDF to `paperreview.ai` using the same HTTP flow as the website:

1) Request a presigned upload URL
2) Upload the PDF directly to S3
3) Confirm the upload to start processing and receive a token

This skill uses a small Python script so it can run deterministically without a browser. The public version requires you to provide your own email when submitting.

## Safety model

- Treat `--submit` as an **irreversible external side effect** (creates a real submission and returns a token).
- Default to `--dry-run` first to validate the file and show what would happen.

## Email policy

The public version does **not** ship with a fixed email address.

- Use `--email you@example.com` when doing a real submission
- Keep your own email out of version-controlled defaults

## How to use

### 1) Dry-run (no network, no submission)

```bash
python scripts/submit_http.py --pdf "/path/to/paper.pdf" --dry-run
```

### 2) Real submit (network + S3 upload + token returned)

```bash
python scripts/submit_http.py --pdf "/path/to/paper.pdf" --venue ICLR --email "you@example.com" --submit
```

By default, after a successful submit the token is also written next to the PDF as:

- `<pdf>.paperreview.token.txt`

To disable token file writing:

```bash
python scripts/submit_http.py --pdf "/path/to/paper.pdf" --venue ICLR --email "you@example.com" --submit --no-token-file
```

### 3) Poll for results (every 10 minutes) and save next to the PDF

When the review is ready, `paperreview.ai` can be queried with:

- `GET /api/review/<token>`
  - `202` means still processing
  - `200` means ready (JSON review payload)

This skill provides a polling script that saves **timestamped** artifacts next to the PDF:

- `<pdf>.paperreview.<timestamp>.json` (raw JSON, includes `_retrieved_at` and `_token`)
- `<pdf>.paperreview.<timestamp>.md` (human-readable Markdown)

Run (default: 10 minutes, up to 48 hours):

```bash
python scripts/watch_review.py --pdf "/path/to/paper.pdf"
```

One-shot check (useful for debugging / cron):

```bash
python scripts/watch_review.py --pdf "/path/to/paper.pdf" --once
```

### Minimal acceptance checks

- Dry-run: exits `0` and prints basic validation info.
- Submit: exits `0` and prints a `token:` line. Save the token immediately.
- Watch: when ready, saves `.json` + `.md` next to the PDF and exits `0`.
