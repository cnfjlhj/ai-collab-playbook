#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import datetime as _dt
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


SEGMENT_TS_LINE_RE = re.compile(r"^\s*时间戳范围:\s*(\[[^\]]+\])\s*$")


@dataclass(frozen=True)
class Segment:
    timestamp_range: str
    title: str
    body: str


def _escape_latex(text: str) -> str:
    # Normalize a few Unicode symbols that may be missing in default Latin fonts.
    text = (
        text.replace("≈", "约")
        .replace("①", "（1）")
        .replace("②", "（2）")
        .replace("③", "（3）")
    )
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciitilde{}"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def _md_inline_to_latex(text: str) -> str:
    """
    Minimal inline conversion:
    - `code` -> \\texttt{code}
    - **bold** -> \\textbf{bold}
    Keep newlines as-is (blank lines create paragraphs in LaTeX).
    """
    code_spans: list[str] = []
    bold_spans: list[str] = []

    code_token_prefix = "\uFFF0CODE"
    bold_token_prefix = "\uFFF0BOLD"
    token_suffix = "\uFFF1"

    def repl_code(m: re.Match[str]) -> str:
        code_spans.append(m.group(1))
        return f"{code_token_prefix}{len(code_spans) - 1}{token_suffix}"

    def repl_bold(m: re.Match[str]) -> str:
        bold_spans.append(m.group(1))
        return f"{bold_token_prefix}{len(bold_spans) - 1}{token_suffix}"

    # Extract code first so ** inside `...` stays literal.
    text = re.sub(r"`([^`]+)`", repl_code, text)
    text = re.sub(r"\*\*(.+?)\*\*", repl_bold, text)

    text = _escape_latex(text)

    for i, content in enumerate(bold_spans):
        token = f"{bold_token_prefix}{i}{token_suffix}"
        text = text.replace(token, r"\textbf{" + _escape_latex(content) + "}")
    for i, content in enumerate(code_spans):
        token = f"{code_token_prefix}{i}{token_suffix}"
        text = text.replace(token, r"\texttt{" + _escape_latex(content) + "}")

    # Emphasize the mentor prefix while keeping exact text.
    text = re.sub(r"(^|\n)【导师评注】", r"\1\\textbf{【导师评注】}", text)
    return text


def _parse_segments(markdown: str) -> list[Segment]:
    text = markdown.replace("\r\n", "\n")
    lines = [ln.rstrip("\n") for ln in text.split("\n")]

    segments: list[Segment] = []
    idx = 0
    n = len(lines)
    while idx < n:
        m = SEGMENT_TS_LINE_RE.match(lines[idx])
        if not m:
            idx += 1
            continue

        ts_range = m.group(1).strip()
        idx += 1
        while idx < n and lines[idx].strip() == "":
            idx += 1
        if idx >= n:
            raise ValueError("Found timestamp range, but missing bold title line.")

        title_line = lines[idx].strip()
        idx += 1
        if title_line.startswith("**") and title_line.endswith("**") and len(title_line) >= 4:
            title = title_line[2:-2].strip()
        else:
            title = title_line.strip()

        body_lines: list[str] = []
        while idx < n and not SEGMENT_TS_LINE_RE.match(lines[idx]):
            body_lines.append(lines[idx])
            idx += 1

        body = "\n".join(body_lines).strip()
        segments.append(Segment(timestamp_range=ts_range, title=title, body=body))

    if not segments:
        raise ValueError("No segments found. Expected lines like: 时间戳范围: [00:00 - 01:23]")
    return segments


def _sanitize_filename_component(text: str, max_len: int = 24) -> str:
    # Keep CJK, letters, digits, underscore, hyphen; turn other chars into underscore.
    cleaned = re.sub(r"[^\w\u4e00-\u9fff\-]+", "_", text.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        cleaned = "视频纪要"
    return cleaned[:max_len].rstrip("_")


def _pick_output_path(outdir: Path, prefix: str, topic: str, now: _dt.datetime) -> Path:
    ts = now.strftime("%Y%m%d_%H%M%S")
    prefix_part = _sanitize_filename_component(prefix, max_len=12)
    topic_part = _sanitize_filename_component(topic, max_len=24)

    base = f"{prefix_part}_{topic_part}_{ts}.pdf"
    candidate = outdir / base
    if not candidate.exists():
        return candidate
    for i in range(2, 100):
        v = outdir / f"{prefix_part}_{topic_part}_{ts}-v{i}.pdf"
        if not v.exists():
            return v
    raise RuntimeError("Too many existing files with the same timestamp; please try again.")


def _render_main_tex(segments: list[Segment], title: str, subtitle: str, now: str) -> str:
    segment_boxes: list[str] = []
    for seg in segments:
        toc_entry = _escape_latex(f"{seg.timestamp_range} {seg.title}")
        segment_boxes.append(r"\phantomsection")
        segment_boxes.append(rf"\addcontentsline{{toc}}{{subsection}}{{{toc_entry}}}")
        segment_boxes.append(r"\begin{tcolorbox}[segmentbox]")
        segment_boxes.append(rf"\textbf{{{_escape_latex('时间戳范围: ' + seg.timestamp_range)}}}")
        segment_boxes.append(r"\par\medskip")
        segment_boxes.append(rf"\textbf{{{_escape_latex(seg.title)}}}")
        segment_boxes.append(r"\par\medskip")
        segment_boxes.append(_md_inline_to_latex(seg.body))
        segment_boxes.append(r"\end{tcolorbox}")
        segment_boxes.append("")

    summary_tex = "\n".join(segment_boxes).rstrip() + "\n"

    return f"""% !TEX program = xelatex
\\documentclass[UTF8,zihao=-4]{{ctexart}}

\\usepackage[a4paper,margin=2cm]{{geometry}}
\\usepackage{{setspace}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}
\\usepackage{{tcolorbox}}
\\tcbuselibrary{{skins,breakable}}
\\usepackage{{fancyhdr}}
\\usepackage{{microtype}}

\\hypersetup{{
  colorlinks=true,
  linkcolor=blue!40!black,
  urlcolor=blue!40!black,
  pdftitle={{{_escape_latex(title)}}},
}}

\\tcbset{{
  segmentbox/.style={{
    enhanced,
    breakable,
    colback=gray!2,
    colframe=gray!35,
    boxrule=0.6pt,
    arc=2mm,
    left=2mm,
    right=2mm,
    top=2mm,
    bottom=2mm,
  }},
}}

\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{{_escape_latex(title)}}}
\\fancyhead[R]{{\\thepage}}
\\renewcommand{{\\headrulewidth}}{{0.4pt}}
\\setlength{{\\headheight}}{{14.5pt}}

\\setlength{{\\parskip}}{{0.6em}}
\\setlength{{\\parindent}}{{0pt}}
\\onehalfspacing

\\begin{{document}}

% ---------------- Cover ----------------
\\begin{{titlepage}}
  \\centering
  \\vspace*{{2.2cm}}
  {{\\Huge\\bfseries {_escape_latex(title)}\\par}}
  \\vspace{{0.8cm}}
  {{\\Large {_escape_latex(subtitle)}\\par}}
  \\vspace{{1.2cm}}
  {{\\large 生成时间：{_escape_latex(now)}\\par}}
  \\vfill
  {{\\small 说明：本文档由 AI 基于带时间戳字幕生成“内容纪要”。默认不附原始逐行字幕材料；如需附录请在需求中明确提出。\\par}}
\\end{{titlepage}}

% --------------- TOC -------------------
\\pagenumbering{{Roman}}
\\setcounter{{tocdepth}}{{2}}
\\tableofcontents
\\clearpage
\\pagenumbering{{arabic}}

\\section*{{视频内容纪要}}
\\addcontentsline{{toc}}{{section}}{{视频内容纪要}}

{summary_tex}

\\end{{document}}
"""


def _run_xelatex(tex_path: Path, work_dir: Path) -> None:
    # Two passes for TOC.
    for _ in range(2):
        subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
            cwd=work_dir,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render timestamped video summary Markdown to a clean PDF.")
    parser.add_argument("--input", type=Path, required=True, help="Path to summary Markdown file (output.md).")
    parser.add_argument("--outdir", type=Path, default=Path("."), help="Directory to write the PDF into.")
    parser.add_argument("--prefix", default="视频纪要", help="Filename prefix (default: 视频纪要).")
    parser.add_argument("--topic", default="", help="Topic for filename/cover (defaults to first segment title).")
    parser.add_argument("--title", default="视频内容纪要（基于字幕）", help="PDF cover title.")
    parser.add_argument("--subtitle", default="", help="PDF cover subtitle (optional).")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"[ERROR] File not found: {args.input}", file=sys.stderr)
        return 2

    md = args.input.read_text(encoding="utf-8")
    segments = _parse_segments(md)

    topic = args.topic.strip() or segments[0].title or "视频纪要"
    now_dt = _dt.datetime.now()
    outdir = args.outdir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    out_pdf = _pick_output_path(outdir, args.prefix, topic, now_dt)
    subtitle = args.subtitle.strip() or f"主题：{topic}"
    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")

    tex = _render_main_tex(segments, args.title, subtitle, now_str)

    with tempfile.TemporaryDirectory(prefix="ts_video_summary_pdf_") as tmp:
        tmp_dir = Path(tmp)
        tex_path = tmp_dir / "main.tex"
        tex_path.write_text(tex, encoding="utf-8")

        try:
            _run_xelatex(tex_path, tmp_dir)
        except subprocess.CalledProcessError:
            # Keep the .tex content in stderr context for debugging without leaking huge logs.
            print("[ERROR] xelatex failed. Re-run with the generated LaTeX if needed.", file=sys.stderr)
            print(f"Temporary LaTeX: {tex_path}", file=sys.stderr)
            return 1

        pdf_src = tmp_dir / "main.pdf"
        out_pdf.write_bytes(pdf_src.read_bytes())

    print(f"✅ PDF 已生成: {out_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

