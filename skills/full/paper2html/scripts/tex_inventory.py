#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


SECTION_RE = re.compile(r"\\(section|subsection|subsubsection)\*?\{([^{}]+)\}")
INCLUDE_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}")
CAPTION_RE = re.compile(r"\\caption(?:\[[^\]]*\])?\{", re.DOTALL)
BEGIN_RE = re.compile(r"\\begin\{(figure\*?|table\*?|algorithm\*?|equation\*?|align\*?)\}")


@dataclass
class Hit:
    kind: str
    file: str
    line: int
    text: str


def clean_tex(text: str) -> str:
    text = re.sub(r"%.*", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def line_no(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def extract_braced(text: str, open_brace_index: int) -> str:
    depth = 0
    start = open_brace_index + 1
    for idx in range(open_brace_index, len(text)):
        char = text[idx]
        if char == "{" and (idx == 0 or text[idx - 1] != "\\"):
            depth += 1
            if depth == 1:
                start = idx + 1
        elif char == "}" and (idx == 0 or text[idx - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[start:idx]
    return text[start : start + 220]


def iter_tex_files(root: Path) -> list[Path]:
    skip = {".git", "__pycache__", "_minted-output"}
    files = []
    for path in root.rglob("*.tex"):
        if any(part in skip for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def analyze(root: Path) -> dict[str, list[Hit] | dict[str, int]]:
    hits: dict[str, list[Hit] | dict[str, int]] = {
        "sections": [],
        "figures": [],
        "tables": [],
        "algorithms": [],
        "equations": [],
        "graphics": [],
        "captions": [],
        "counts": {},
    }
    counts: dict[str, int] = {}
    for path in iter_tex_files(root):
        rel = str(path.relative_to(root))
        text = path.read_text(encoding="utf-8", errors="replace")

        for match in SECTION_RE.finditer(text):
            hits["sections"].append(
                Hit(match.group(1), rel, line_no(text, match.start()), clean_tex(match.group(2)))
            )

        for match in INCLUDE_RE.finditer(text):
            hits["graphics"].append(
                Hit("includegraphics", rel, line_no(text, match.start()), clean_tex(match.group(1)))
            )

        for match in CAPTION_RE.finditer(text):
            open_brace = text.find("{", match.start())
            caption = clean_tex(extract_braced(text, open_brace))
            hits["captions"].append(
                Hit("caption", rel, line_no(text, match.start()), caption[:420])
            )

        for match in BEGIN_RE.finditer(text):
            env = match.group(1)
            counts[env] = counts.get(env, 0) + 1
            bucket = (
                "figures"
                if env.startswith("figure")
                else "tables"
                if env.startswith("table")
                else "algorithms"
                if env.startswith("algorithm")
                else "equations"
            )
            snippet = clean_tex(text[match.start() : match.start() + 260])
            hits[bucket].append(Hit(env, rel, line_no(text, match.start()), snippet))

    counts["tex_files"] = len(iter_tex_files(root))
    hits["counts"] = counts
    return hits


def md_table(title: str, rows: list[Hit], columns: tuple[str, str] = ("Kind", "Text")) -> str:
    lines = [f"## {title}", "", f"| {columns[0]} | File:line | {columns[1]} |", "| --- | --- | --- |"]
    for hit in rows:
        lines.append(
            f"| {hit.kind} | `{hit.file}:{hit.line}` | {hit.text.replace('|', '/')} |"
        )
    if not rows:
        lines.append("|  |  |  |")
    lines.append("")
    return "\n".join(lines)


def write_markdown(root: Path, out: Path, hits: dict[str, list[Hit] | dict[str, int]]) -> None:
    counts = hits["counts"]
    assert isinstance(counts, dict)
    parts = [
        "# TeX Inventory",
        "",
        f"Root: `{root}`",
        "",
        "## Counts",
        "",
        "| Item | Count |",
        "| --- | ---: |",
    ]
    for key in sorted(counts):
        parts.append(f"| {key} | {counts[key]} |")
    parts.append("")

    for key, title in [
        ("sections", "Section Outline"),
        ("graphics", "Included Graphics"),
        ("captions", "Captions"),
        ("figures", "Figure Environments"),
        ("tables", "Table Environments"),
        ("algorithms", "Algorithm Environments"),
        ("equations", "Equation/Align Environments"),
    ]:
        rows = hits[key]
        assert isinstance(rows, list)
        parts.append(md_table(title, rows))

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a TeX inventory for paper2html.")
    parser.add_argument("tex_root", help="Root containing TeX source.")
    parser.add_argument("--out", help="Markdown output path.")
    parser.add_argument("--json", dest="json_out", help="Optional JSON output path.")
    args = parser.parse_args()

    root = Path(args.tex_root).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Missing TeX root: {root}")
    hits = analyze(root)

    out = Path(args.out).expanduser().resolve() if args.out else root / "tex-inventory.md"
    write_markdown(root, out, hits)
    print(out)

    if args.json_out:
        json_out = Path(args.json_out).expanduser().resolve()
        json_out.parent.mkdir(parents=True, exist_ok=True)
        serializable = {
            key: [asdict(hit) for hit in value] if isinstance(value, list) else value
            for key, value in hits.items()
        }
        json_out.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json_out)


if __name__ == "__main__":
    main()
