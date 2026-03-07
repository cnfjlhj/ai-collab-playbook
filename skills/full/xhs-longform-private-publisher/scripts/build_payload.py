#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TITLE_RE = re.compile(r"^\s*#\s+(?P<title>.+?)\s*$")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^\)]+\)")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a Xiaohongshu longform payload from Markdown and ordered images."
    )
    parser.add_argument("markdown_path", type=Path, help="Path to the source Markdown file.")
    parser.add_argument(
        "--image-dir",
        type=Path,
        help="Directory containing inline images. Files are sorted numerically by filename.",
    )
    parser.add_argument(
        "--images",
        nargs="*",
        type=Path,
        default=None,
        help="Explicit image paths in insertion order.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Optional JSON output path. Defaults to stdout.",
    )
    parser.add_argument(
        "--title",
        help="Optional title override. Defaults to the first H1 in the Markdown file.",
    )
    parser.add_argument(
        "--allow-count-mismatch",
        action="store_true",
        help="Allow image count to differ from Markdown image marker count.",
    )
    return parser.parse_args()


def load_renderer():
    try:
        import markdown
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency 'markdown'. Install it with `python -m pip install markdown`."
        ) from exc

    def render(text: str) -> str:
        if not text.strip():
            return ""
        return markdown.markdown(
            text,
            extensions=["extra", "fenced_code", "tables", "sane_lists", "nl2br"],
        )

    return render


def image_sort_key(path: Path):
    numbers = tuple(int(part) for part in re.findall(r"\d+", path.stem))
    if numbers:
        return (0, numbers, path.name.lower())
    return (1, (), path.name.lower())


def collect_images(image_dir: Path | None, image_paths: list[Path] | None) -> list[Path]:
    if image_dir and image_paths:
        raise SystemExit("Use either --image-dir or --images, not both.")
    if image_paths:
        missing = [str(path) for path in image_paths if not path.is_file()]
        if missing:
            raise SystemExit(f"Image file(s) not found: {', '.join(missing)}")
        return image_paths
    if image_dir:
        if not image_dir.is_dir():
            raise SystemExit(f"Image directory not found: {image_dir}")
        files = [
            path
            for path in image_dir.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
        ]
        return sorted(files, key=image_sort_key)
    return []


def extract_title_and_body(markdown_text: str, fallback_title: str) -> tuple[str, str]:
    lines = markdown_text.splitlines()
    for index, line in enumerate(lines):
        match = TITLE_RE.match(line)
        if match:
            title = match.group("title").strip()
            body_lines = lines[:index] + lines[index + 1 :]
            while body_lines and not body_lines[0].strip():
                body_lines.pop(0)
            return title, "\n".join(body_lines)
    return fallback_title, markdown_text.strip()


def split_markdown_parts(body: str) -> tuple[list[str], list[str]]:
    parts: list[str] = []
    markers: list[str] = []
    current: list[str] = []
    for line in body.splitlines():
        if IMAGE_RE.search(line.strip()):
            parts.append("\n".join(current).strip())
            markers.append(line.strip())
            current = []
            continue
        current.append(line)
    parts.append("\n".join(current).strip())
    return parts, markers


def build_payload(
    markdown_path: Path,
    image_dir: Path | None,
    image_paths: list[Path] | None,
    title_override: str | None,
    allow_count_mismatch: bool,
) -> dict:
    if not markdown_path.is_file():
        raise SystemExit(f"Markdown file not found: {markdown_path}")

    source_text = markdown_path.read_text(encoding="utf-8")
    fallback_title = markdown_path.stem.replace("_", " ").strip() or "未命名长文"
    detected_title, body = extract_title_and_body(source_text, fallback_title)
    title = title_override.strip() if title_override else detected_title
    parts, markers = split_markdown_parts(body)
    images = collect_images(image_dir, image_paths)

    if markers and len(markers) != len(images) and not allow_count_mismatch:
        raise SystemExit(
            "Markdown 图片占位数量与图片文件数量不一致："
            f"占位 {len(markers)}，图片 {len(images)}。"
            "如属有意行为，请显式传入 --allow-count-mismatch。"
        )

    render = load_renderer()
    html_parts = [render(part) for part in parts]
    return {
        "title": title,
        "parts": html_parts,
        "images": [str(path) for path in images],
    }


def main() -> int:
    args = parse_args()
    payload = build_payload(
        markdown_path=args.markdown_path,
        image_dir=args.image_dir,
        image_paths=args.images,
        title_override=args.title,
        allow_count_mismatch=args.allow_count_mismatch,
    )
    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
    else:
        sys.stdout.write(serialized + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
