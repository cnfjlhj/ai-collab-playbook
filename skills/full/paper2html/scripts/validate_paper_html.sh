#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'USAGE'
Usage:
  validate_paper_html.sh <index.html> [--public]

Checks:
  - file exists and is HTML
  - no common placeholders
  - no private local-source leaks in public mode
  - KaTeX auto-render creates math nodes and no katex-error
  - desktop and mobile screenshots can be rendered by Chrome
USAGE
}

HTML_PATH="${1:-}"
MODE_PUBLIC=0
shift || true
for arg in "$@"; do
  case "$arg" in
    --public) MODE_PUBLIC=1 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$HTML_PATH" ]]; then usage; exit 2; fi
if [[ ! -f "$HTML_PATH" ]]; then echo "Missing HTML file: $HTML_PATH" >&2; exit 1; fi
if [[ "${HTML_PATH##*.}" != "html" ]]; then echo "Expected .html: $HTML_PATH" >&2; exit 1; fi

python3 - "$HTML_PATH" "$MODE_PUBLIC" <<'PY'
import re
import sys
from pathlib import Path

html_path = Path(sys.argv[1])
public = sys.argv[2] == "1"
html = html_path.read_text(encoding="utf-8", errors="replace")

# Base64 payloads can accidentally contain strings like TODO. Do static text
# checks on a masked copy, while browser checks still use the original file.
masked = re.sub(
    r"""(?P<prefix>\b(?:src|href)=["'])data:[^"']+(?P<suffix>["'])""",
    r"\g<prefix>data:masked\g<suffix>",
    html,
    flags=re.IGNORECASE,
)

patterns = [
    ("placeholder", re.compile(r"(__[A-Z0-9_]+__|TODO|PLACEHOLDER|FIXME|katex-error)")),
]

if public:
    patterns.append(
        (
            "local/private source leak",
            re.compile(
                r"(/home/|file://|main\.tex|main\.pdf|sections/|appendices/|figures/|"
                r"本地论文|本地 LaTeX|本地 PDF|未做外部 Web 检索|"
                r"private review draft|not public-published)"
            ),
        )
    )

for label, pattern in patterns:
    for line_no, line in enumerate(masked.splitlines(), start=1):
        match = pattern.search(line)
        if match:
            print(f"{html_path}:{line_no}: {label}: {match.group(0)}", file=sys.stderr)
            raise SystemExit(1)
PY

if ! command -v google-chrome >/dev/null 2>&1; then
  echo "google-chrome not found; skipped browser render checks." >&2
  exit 0
fi

tmpdir="$(mktemp -d)"
cleanup() {
  if [[ -n "${server_pid:-}" ]]; then kill "$server_pid" >/dev/null 2>&1 || true; fi
}
trap cleanup EXIT

src_dir="$(cd "$(dirname "$HTML_PATH")" && pwd)"
src_file="$(basename "$HTML_PATH")"
port="$(python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
)"

(cd "$src_dir" && python3 -m http.server "$port" --bind 127.0.0.1 >"$tmpdir/server.log" 2>&1) &
server_pid="$!"
sleep 0.5
url="http://127.0.0.1:${port}/${src_file}"

dom="$tmpdir/dom.txt"
google-chrome --headless=new --disable-gpu --no-sandbox --dump-dom "$url" >"$dom" 2>"$tmpdir/chrome-dom.err"

if grep -q 'katex-error' "$dom"; then
  echo "Rendered DOM contains katex-error." >&2
  exit 1
fi
if ! grep -q 'class="katex' "$dom"; then
  echo "Rendered DOM contains no KaTeX nodes; check math initialization or source formulas." >&2
  exit 1
fi

google-chrome --headless=new --disable-gpu --no-sandbox --window-size=1440,1200 --screenshot="$tmpdir/desktop.png" "$url" >/dev/null 2>"$tmpdir/chrome-desktop.err"

python3 - "$url" "$tmpdir/mobile.png" <<'PY'
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

url, out = sys.argv[1], Path(sys.argv[2])
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 390, "height": 1000}, device_scale_factor=1, is_mobile=True)
    page.goto(url, wait_until="networkidle")
    dims = page.evaluate("""() => ({
      innerWidth,
      docClient: document.documentElement.clientWidth,
      docScroll: document.documentElement.scrollWidth,
      bodyScroll: document.body.scrollWidth
    })""")
    page.screenshot(path=str(out), full_page=False)
    browser.close()

print(dims)
if dims["docScroll"] > dims["innerWidth"]:
    raise SystemExit(f"document overflows horizontally: {dims}")
PY

echo "paper2html validation passed"
echo "Desktop screenshot: $tmpdir/desktop.png"
echo "Mobile screenshot:  $tmpdir/mobile.png"
