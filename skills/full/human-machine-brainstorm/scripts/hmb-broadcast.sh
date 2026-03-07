#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  hmb-broadcast.sh [--to "claude opencode"] [--timeout 3600] [--file prompt.md]

Notes:
  - Reads the message from --file, otherwise from stdin.
  - Sends via: CCB_CALLER=codex ask <provider> ...
  - Requires a running CCB session in the current project directory.
EOF
}

to_providers="claude opencode"
timeout_s="3600"
file_path=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --to) to_providers="${2:-}"; shift 2 ;;
    --timeout) timeout_s="${2:-}"; shift 2 ;;
    --file) file_path="${2:-}"; shift 2 ;;
    *) echo "[hmb-broadcast] unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -n "$file_path" ]]; then
  if [[ ! -f "$file_path" ]]; then
    echo "[hmb-broadcast] file not found: $file_path" >&2
    exit 2
  fi
  message="$(cat "$file_path")"
else
  if [[ -t 0 ]]; then
    echo "[hmb-broadcast] no --file and stdin is TTY; nothing to send" >&2
    usage
    exit 2
  fi
  message="$(cat)"
fi

message="${message%$'\n'}"
if [[ -z "${message//[$' \t\r\n']/}" ]]; then
  echo "[hmb-broadcast] empty message" >&2
  exit 2
fi

for provider in $to_providers; do
  echo "[hmb-broadcast] -> $provider"
  printf '%s\n' "$message" | CCB_CALLER=codex ask "$provider" --timeout "$timeout_s"
done

