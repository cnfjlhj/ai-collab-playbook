#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'USAGE'
Usage:
  publish_paper2html.sh <index.html> --to=topic/series/slug [options]

One command from a finished paper2html page to a compatible /research/ repo:
  1. validate the HTML in public mode
  2. import it into the target research path
  3. format, check, commit only touched research files, and push when --ship is used
  4. optionally wait for deployment and verify the remote URL when --ship is used

Environment:
  PAPER2HTML_BLOG_ROOT       Required. Repo containing `pnpm research:publish`.
  PAPER2HTML_PUBLIC_BASE_URL Optional. Base URL used for final URL output and remote checks.
                              Example: https://example.com/research
  PAPER2HTML_DEPLOY_WORKFLOW Optional. GitHub Actions workflow name for --ship watch.

Required:
  <index.html>              Finished paper2html page
  --to=topic/series/slug    Destination path under /research/

Forwarded metadata:
  --title="Readable title"
  --description="Short summary"
  --date=YYYY-MM-DD
  --tags=a,b,c
  --topic-title="中文课题名"
  --series-title="中文系列名"
  --source="https://..."

Modes:
  --ship                    Validate, import, check, commit, and push
  --check                   Validate, import, and run local checks
  --dry-run                 Validate and print target without writing
  --no-watch                Do not wait for the deploy workflow after --ship
  --no-remote-verify        Do not curl-check the public URL after --ship
  --remote-verify           Curl-check the public URL even when not shipping
  --skip-validate           Skip paper2html browser/public validation
  --allow-private-evidence  Forwarded to blog importer; avoid for public pages

Examples:
  PAPER2HTML_BLOG_ROOT=/path/to/blog publish_paper2html.sh /tmp/paper/index.html --to=topic/series/page --check
  PAPER2HTML_BLOG_ROOT=/path/to/blog PAPER2HTML_PUBLIC_BASE_URL=https://example.com/research publish_paper2html.sh /tmp/paper/index.html --to=topic/series/page --ship
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLOG_ROOT="${PAPER2HTML_BLOG_ROOT:-}"
PUBLIC_BASE_URL="${PAPER2HTML_PUBLIC_BASE_URL:-}"
DEPLOY_WORKFLOW="${PAPER2HTML_DEPLOY_WORKFLOW:-deploy-cloudflare-pages.yml}"
VALIDATOR="$SCRIPT_DIR/validate_paper_html.sh"

HTML_PATH=""
SKIP_VALIDATE=0
SHIP=0
DRY_RUN=0
WATCH_DEPLOY=1
REMOTE_VERIFY=""
TO_VALUE=""
RESEARCH_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      usage
      exit 0
      ;;
    --skip-validate)
      SKIP_VALIDATE=1
      shift
      ;;
    --no-watch)
      WATCH_DEPLOY=0
      shift
      ;;
    --watch)
      WATCH_DEPLOY=1
      shift
      ;;
    --no-remote-verify)
      REMOTE_VERIFY=0
      shift
      ;;
    --remote-verify)
      REMOTE_VERIFY=1
      shift
      ;;
    --to=*)
      TO_VALUE="${1#--to=}"
      RESEARCH_ARGS+=("$1")
      shift
      ;;
    --title=*|--description=*|--date=*|--tags=*|--topic-title=*|--series-title=*|--source=*|--message=*)
      RESEARCH_ARGS+=("$1")
      shift
      ;;
    --to)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        usage
        exit 2
      fi
      TO_VALUE="$2"
      RESEARCH_ARGS+=("$1" "$2")
      shift 2
      ;;
    --title|--description|--date|--tags|--topic-title|--series-title|--source|--message)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for $1" >&2
        usage
        exit 2
      fi
      RESEARCH_ARGS+=("$1" "$2")
      shift 2
      ;;
    --ship)
      SHIP=1
      if [[ -z "$REMOTE_VERIFY" ]]; then
        REMOTE_VERIFY=1
      fi
      RESEARCH_ARGS+=("$1")
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      RESEARCH_ARGS+=("$1")
      shift
      ;;
    --check|--allow-private-evidence)
      RESEARCH_ARGS+=("$1")
      shift
      ;;
    --*)
      echo "Unknown option: $1" >&2
      usage
      exit 2
      ;;
    *)
      if [[ -z "$HTML_PATH" ]]; then
        HTML_PATH="$1"
        shift
      else
        echo "Unexpected positional argument: $1" >&2
        usage
        exit 2
      fi
      ;;
  esac
done

if [[ -z "$HTML_PATH" ]]; then
  echo "Missing index.html." >&2
  usage
  exit 2
fi

if [[ ! -f "$HTML_PATH" ]]; then
  echo "Missing HTML file: $HTML_PATH" >&2
  exit 1
fi

if [[ "${HTML_PATH##*.}" != "html" ]]; then
  echo "Expected .html file: $HTML_PATH" >&2
  exit 1
fi

has_to=0
for arg in "${RESEARCH_ARGS[@]}"; do
  if [[ "$arg" == --to || "$arg" == --to=* ]]; then
    has_to=1
    break
  fi
done

if [[ "$has_to" -ne 1 ]]; then
  echo "Missing --to=topic/series/slug." >&2
  usage
  exit 2
fi

normalize_research_path() {
  python3 - "$1" <<'PY'
import re
import sys

value = sys.argv[1].strip()
value = re.sub(r"^https?://[^/]+/research/", "", value, flags=re.I)
value = re.sub(r"[?#].*$", "", value)
value = re.sub(r"^/?research/", "", value, flags=re.I)
value = re.sub(r"^public/research/", "", value, flags=re.I)
value = re.sub(r"/index\.html$", "", value, flags=re.I)
segments = [segment for segment in value.strip("/").split("/") if segment]

if len(segments) < 2:
    raise SystemExit("research path must include at least topic and page slug")

for segment in segments:
    if segment in {".", ".."} or not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", segment):
        raise SystemExit(f"invalid research path segment: {segment}")

print("/".join(segments))
PY
}

wait_for_deploy_run() {
  local sha="$1"
  if ! command -v gh >/dev/null 2>&1; then
    echo "[paper2html] gh not found; skipped deploy workflow watch"
    return 0
  fi

  local deadline=$((SECONDS + 120))
  local run_id=""

  echo "[paper2html] waiting for deploy workflow '$DEPLOY_WORKFLOW' for $sha"
  while [[ "$SECONDS" -lt "$deadline" ]]; do
    run_id="$(
      gh run list \
        --workflow "$DEPLOY_WORKFLOW" \
        --limit 20 \
        --json databaseId,headSha \
        --jq ".[] | select(.headSha == \"$sha\") | .databaseId" \
        2>/dev/null \
        | head -n 1 \
        || true
    )"

    if [[ -n "$run_id" ]]; then
      gh run watch "$run_id" --exit-status
      return 0
    fi

    sleep 5
  done

  echo "[paper2html] deploy workflow did not appear within 120s; skipped watch"
}

if [[ -z "$BLOG_ROOT" ]]; then
  echo "PAPER2HTML_BLOG_ROOT is required for publishing." >&2
  exit 2
fi

if [[ ! -d "$BLOG_ROOT" ]]; then
  echo "Target repo does not exist: $BLOG_ROOT" >&2
  exit 1
fi

if [[ "$SKIP_VALIDATE" -ne 1 ]]; then
  "$VALIDATOR" "$HTML_PATH" --public
else
  echo "[paper2html] skipped HTML validation"
fi

cd "$BLOG_ROOT"
before_sha="$(git rev-parse HEAD)"
pnpm research:publish "$HTML_PATH" "${RESEARCH_ARGS[@]}"
after_sha="$(git rev-parse HEAD)"

if [[ "$DRY_RUN" -eq 1 ]]; then
  exit 0
fi

if [[ -z "$REMOTE_VERIFY" ]]; then
  REMOTE_VERIFY=0
fi

research_path="$(normalize_research_path "$TO_VALUE")"
pnpm research verify "$research_path"

if [[ "$SHIP" -eq 1 ]]; then
  if [[ "$after_sha" != "$before_sha" ]]; then
    if [[ "$WATCH_DEPLOY" -eq 1 ]]; then
      wait_for_deploy_run "$after_sha"
    fi
  else
    echo "[paper2html] no new commit was created; skipped deploy workflow watch"
  fi
fi

if [[ "$REMOTE_VERIFY" -eq 1 ]]; then
  pnpm research verify "$research_path" --remote
fi

if [[ -n "$PUBLIC_BASE_URL" ]]; then
  echo "[paper2html] public URL: ${PUBLIC_BASE_URL%/}/${research_path}/"
else
  echo "[paper2html] published path: /research/${research_path}/"
fi
