#!/usr/bin/env bash
set -euo pipefail

slug="${1:-}"
if [[ -z "${slug// /}" ]]; then
  echo "Usage: hmb-init.sh <topic-slug>" >&2
  echo "Example: hmb-init.sh ccb-requirements-brainstorm" >&2
  exit 2
fi

date_prefix="$(date +%F)"
base_dir="${HOME}/ccb-startups"
root_dir="${base_dir}/${date_prefix}-${slug}"

mkdir -p "${root_dir}/.ccb/spec" "${root_dir}/.ccb/history" "${root_dir}/.ccb/bin" "${root_dir}/.ccb/prototypes"

cat > "${root_dir}/.ccb/spec/overview.md" <<'EOF'
# Spec Overview (v0)

> Single source of truth for final handoff.
> Editing owner: **Claude Code** (other models propose changes via questions/reviews).

## 0. Metadata

- Topic:
- Version: v0 (draft)
- Status: drafting | review | final
- Last updated:
- Owners:
  - Facilitator / Dispatcher: Codex
  - Scribe / Spec owner: Claude Code
  - Divergent thinker / Prototypes: OpenCode (Gemini)

## 1. Problem Statement

- What problem are we solving?
- Why now?
- What does “success” look like?

## 2. Scope

### In scope
- ...

### Out of scope
- ...

## 3. Users & Use Cases
- Primary user(s):
- Key scenarios:

## 4. Constraints
- Time:
- Cost:
- Security / privacy:
- Platform / environment:
- Dependencies:

## 5. Proposed Solution (High-level)

- One-paragraph summary:
- Architecture (ASCII sketch):

```
[client] -> [api] -> [service] -> [storage]
```

## 6. Detailed Design

### 6.1 Data model

### 6.2 APIs / Interfaces

### 6.3 Workflow / State machine

## 7. Edge Cases & Failure Modes
- ...

## 8. Validation / Acceptance Criteria
- Must-pass checks:

EOF

cat > "${root_dir}/.ccb/spec/open_questions.md" <<'EOF'
# Open Questions

Status: `open` | `answered` | `decided` | `blocked` | `ignored`

| ID | Priority | Question | Status | Answer (short) | Owner | Links |
|---:|:--:|---|:--:|---|---|---|
| Q001 | P0 | What is the primary user + success metric? | open |  | user |  |
| Q002 | P0 | What is the hard constraint (time/cost/security)? | open |  | user |  |
| Q003 | P1 | What is explicitly out of scope? | open |  | user |  |

EOF

cat > "${root_dir}/.ccb/spec/decisions.md" <<'EOF'
# Decisions (ADR-lite)

## D### - <title>

- Date:
- Status: proposed | accepted | superseded
- Related questions:
- Decision:
- Rationale:
- Alternatives considered:
- Consequences / trade-offs:
- Revisit when:

EOF

cat > "${root_dir}/.ccb/spec/changelog.md" <<EOF
# Spec Changelog

## v0 (draft) - ${date_prefix}

- Initialized HMB spec template.

EOF

cat > "${root_dir}/.ccb/bin/round-save.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HISTORY_DIR="$ROOT_DIR/.ccb/history"

LAST_N="${1:-20}"
if ! [[ "$LAST_N" =~ ^[0-9]+$ ]]; then
  echo "[round-save] LAST_N must be an integer, got: $LAST_N" >&2
  exit 2
fi

mkdir -p "$HISTORY_DIR"

if ! command -v ctx-transfer >/dev/null 2>&1; then
  echo "[round-save] ctx-transfer not found in PATH." >&2
  exit 127
fi

ts="$(date +%Y%m%d-%H%M%S)"

save_one() {
  local provider="$1"
  local out="$HISTORY_DIR/${provider}-${ts}.md"
  local err="$HISTORY_DIR/${provider}-${ts}.err"
  if ctx-transfer --from "$provider" --last "$LAST_N" --output "$out" --quiet 2>"$err"; then
    if [[ -s "$err" ]]; then
      echo "[round-save] note: $provider had stderr -> $err" >&2
    else
      rm -f "$err" || true
    fi
    echo "[round-save] saved $provider -> $out"
    return 0
  fi
  local note="$HISTORY_DIR/${provider}-${ts}-NOSESSION.txt"
  printf '%s\n' \
    "No session found for provider=$provider in dir=$ROOT_DIR" \
    "Hint: start CCB in this directory first (ccb claude codex opencode cmd)." \
    "Details (stderr): $err" \
    >"$note"
  echo "[round-save] warn: no $provider session; wrote $note" >&2
  return 0
}

save_one "claude"
save_one "codex"
save_one "opencode"

echo "[round-save] done (last=$LAST_N)"
EOF

chmod +x "${root_dir}/.ccb/bin/round-save.sh"

echo ""
echo "[HMB] Initialized:"
echo "  ${root_dir}"
echo ""
echo "[HMB] Next:"
echo "  cd \"${root_dir}\""
echo "  ccb claude codex opencode cmd"
echo ""

