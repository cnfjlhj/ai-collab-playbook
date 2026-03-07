#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  hmb-route-answers.sh --answers answers.txt [--send] [--timeout 3600]

answers.txt format (one per line):
  C-Q01: ...
  C-Q02: ...
  O-Q01: ...
  SHARED: ...

Behavior:
  - Builds two routed messages (Claude and OpenCode).
  - If --send is set, sends via: CCB_CALLER=codex ask <provider> ...
  - Otherwise prints the routed payloads to stdout.
EOF
}

answers_path=""
send="0"
timeout_s="3600"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --answers) answers_path="${2:-}"; shift 2 ;;
    --send) send="1"; shift 1 ;;
    --timeout) timeout_s="${2:-}"; shift 2 ;;
    *) echo "[hmb-route] unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$answers_path" || ! -f "$answers_path" ]]; then
  echo "[hmb-route] --answers file required" >&2
  usage
  exit 2
fi

shared="$(grep -E '^SHARED:' "$answers_path" 2>/dev/null || true)"
claude_lines="$(grep -E '^C-Q[0-9]+:' "$answers_path" 2>/dev/null || true)"
opencode_lines="$(grep -E '^O-Q[0-9]+:' "$answers_path" 2>/dev/null || true)"

claude_payload=$(
  cat <<EOF
HMB routed answers (Claude)

${shared}

${claude_lines}
EOF
)
opencode_payload=$(
  cat <<EOF
HMB routed answers (OpenCode)

${shared}

${opencode_lines}
EOF
)

if [[ "$send" == "1" ]]; then
  printf '%s\n' "$claude_payload" | CCB_CALLER=codex ask claude --timeout "$timeout_s"
  printf '%s\n' "$opencode_payload" | CCB_CALLER=codex ask opencode --timeout "$timeout_s"
  exit 0
fi

echo "----- CLAUDE -----"
printf '%s\n' "$claude_payload"
echo "----- OPENCODE -----"
printf '%s\n' "$opencode_payload"
