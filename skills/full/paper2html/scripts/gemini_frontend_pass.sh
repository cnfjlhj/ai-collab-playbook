#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  gemini_frontend_pass.sh <index.html> [options]

Options:
  --draft PATH       Draft HTML path. Default: <dir>/index.gemini-draft.html
  --reference PATH   Optional reference HTML/screenshot/text file for visual style
  --material PATH    Paper material pack / notes / extracted source summary; repeatable
  --no-auto-material Do not auto-attach common notes from <dir>/notes
  --notes PATH       Sidecar output notes. Default: <dir>/notes/gemini-frontend-pass.md
  --prompt PATH      Prompt template. Default: paper2html/prompts/gemini-initial-html.md
  --timeout SEC      Timeout for the Gemini sidecar run. Default: 240
  --role NAME        OpenCode sidecar role. Default: frontend
  --skip-permissions Pass --dangerously-skip-permissions to the sidecar runner
  --dry-run          Create draft/notes and print the final prompt without calling Gemini
  -h, --help         Show this help

Creates a Gemini-edited initial HTML draft from an existing paper2html page.
The source index.html is not edited by this script.

Set OPENCODE_SIDECAR_RUNNER when the OpenCode sidecar runner is not installed
at $HOME/.codex/skills/opencode-sidecar/scripts/run-opencode-sidecar.sh.
EOF
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd "$script_dir/.." && pwd)"
default_prompt="$skill_root/prompts/gemini-initial-html.md"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 2
fi

html_path=""
draft_path=""
reference_path=""
notes_path=""
prompt_template="$default_prompt"
timeout_seconds=240
role="frontend"
auto_material=1
dry_run=0
skip_permissions=0
declare -a material_files=()

html_path="$1"
shift

while (($#)); do
  case "$1" in
    --draft)
      draft_path="${2:?missing value for --draft}"
      shift 2
      ;;
    --reference)
      reference_path="${2:?missing value for --reference}"
      shift 2
      ;;
    --material)
      material_files+=("${2:?missing value for --material}")
      shift 2
      ;;
    --no-auto-material)
      auto_material=0
      shift
      ;;
    --notes)
      notes_path="${2:?missing value for --notes}"
      shift 2
      ;;
    --prompt)
      prompt_template="${2:?missing value for --prompt}"
      shift 2
      ;;
    --timeout)
      timeout_seconds="${2:?missing value for --timeout}"
      shift 2
      ;;
    --role)
      role="${2:?missing value for --role}"
      shift 2
      ;;
    --skip-permissions)
      skip_permissions=1
      shift
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

html_path="$(realpath "$html_path")"
if [[ ! -f "$html_path" ]]; then
  echo "HTML file not found: $html_path" >&2
  exit 2
fi

html_dir="$(dirname "$html_path")"
if [[ -z "$draft_path" ]]; then
  draft_path="$html_dir/index.gemini-draft.html"
else
  draft_path="$(realpath -m "$draft_path")"
fi
if [[ -z "$notes_path" ]]; then
  notes_path="$html_dir/notes/gemini-frontend-pass.md"
else
  notes_path="$(realpath -m "$notes_path")"
fi

if [[ -n "$reference_path" ]]; then
  reference_path="$(realpath "$reference_path")"
  if [[ ! -f "$reference_path" ]]; then
    echo "Reference file not found: $reference_path" >&2
    exit 2
  fi
fi

prompt_template="$(realpath "$prompt_template")"
if [[ ! -f "$prompt_template" ]]; then
  echo "Prompt template not found: $prompt_template" >&2
  exit 2
fi

if [[ "$auto_material" -eq 1 ]]; then
  for candidate in \
    "$html_dir/notes/material-pack.md" \
    "$html_dir/notes/tex-inventory.md" \
    "$html_dir/notes/figure-table-map.md" \
    "$html_dir/notes/source-boundary.md"; do
    if [[ -f "$candidate" ]]; then
      material_files+=("$candidate")
    fi
  done
fi

declare -A seen_material=()
declare -a resolved_material_files=()
for i in "${!material_files[@]}"; do
  resolved="$(realpath "${material_files[$i]}")"
  if [[ ! -f "$resolved" ]]; then
    echo "Material file not found: $resolved" >&2
    exit 2
  fi
  if [[ -z "${seen_material[$resolved]+x}" ]]; then
    seen_material[$resolved]=1
    resolved_material_files+=("$resolved")
  fi
done
material_files=("${resolved_material_files[@]}")

runner="${OPENCODE_SIDECAR_RUNNER:-$HOME/.codex/skills/opencode-sidecar/scripts/run-opencode-sidecar.sh}"
if [[ ! -x "$runner" ]]; then
  echo "OpenCode sidecar runner not executable: $runner" >&2
  echo "Set OPENCODE_SIDECAR_RUNNER=/path/to/run-opencode-sidecar.sh or use --dry-run." >&2
  exit 127
fi

mkdir -p "$(dirname "$draft_path")" "$(dirname "$notes_path")"
cp "$html_path" "$draft_path"

prompt_file="$(mktemp "${TMPDIR:-/tmp}/paper2html-gemini-frontend.XXXXXX.md")"
trap 'rm -f "$prompt_file"' EXIT

cat "$prompt_template" >"$prompt_file"
cat >>"$prompt_file" <<EOF

---

Execution context for this OpenCode run:

You are the Gemini initial HTML pass for a paper2html artifact.

Edit only this draft HTML file:
$draft_path

Do not edit the source file:
$html_path

Treat this draft as the target single-file index.html for your generation pass.
If the prompt template asks you to output index.html, implement that by editing
the draft file above rather than printing a full HTML blob in chat.

Use attached material files as the paper evidence basis. If a claim is not
supported by the attached materials or the existing draft, mark it for Codex
review instead of inventing details.

After editing the draft, return a concise changelog with:
1. The visual system changes.
2. The content/depth changes you made from attached materials.
3. Risks Codex should verify before publishing.
EOF

if [[ -n "$reference_path" ]]; then
  cat >>"$prompt_file" <<EOF

Optional visual reference:
$reference_path

Use it as visual inspiration only. Do not copy private content or unsupported claims from it.
EOF
fi

if ((${#material_files[@]})); then
  {
    echo
    echo "Attached paper material files:"
    for path in "${material_files[@]}"; do
      echo "- $path"
    done
  } >>"$prompt_file"
else
  cat >>"$prompt_file" <<'EOF'

No extra material files were attached. Work only from the current draft and
explicitly mark content gaps for Codex review.
EOF
fi

cmd=(
  timeout "${timeout_seconds}s"
  "$runner"
  --dir "$html_dir"
  --role "$role"
  --file "$draft_path"
  --message-file "$prompt_file"
)
if [[ "$skip_permissions" -eq 1 ]]; then
  cmd+=(--dangerously-skip-permissions)
fi
if [[ -n "$reference_path" ]]; then
  cmd+=(--file "$reference_path")
fi
for path in "${material_files[@]}"; do
  cmd+=(--file "$path")
done

if [[ "$dry_run" -eq 1 ]]; then
  {
    echo "Dry run: Gemini sidecar was not executed."
    echo
    echo "Draft:"
    echo "$draft_path"
    echo
    echo "Source:"
    echo "$html_path"
    echo
    echo "Reference:"
    echo "${reference_path:-<none>}"
    echo
    echo "Material files:"
    if ((${#material_files[@]})); then
      for path in "${material_files[@]}"; do
        echo "- $path"
      done
    else
      echo "<none>"
    fi
    echo
    echo "Command:"
    printf '%q ' "${cmd[@]}"
    echo
    echo
    echo "Final prompt:"
    echo "=========="
    cat "$prompt_file"
  } >"$notes_path"
  printf 'draft=%s\n' "$draft_path"
  printf 'notes=%s\n' "$notes_path"
  printf 'exit=0\n'
  exit 0
fi

set +e
"${cmd[@]}" >"$notes_path" 2>&1
exit_code=$?
set -e

if cmp -s "$html_path" "$draft_path"; then
  {
    echo
    echo "---"
    echo "Warning: Gemini sidecar did not modify the draft HTML."
  } >>"$notes_path"
fi

printf 'draft=%s\n' "$draft_path"
printf 'notes=%s\n' "$notes_path"
printf 'exit=%s\n' "$exit_code"
exit "$exit_code"
