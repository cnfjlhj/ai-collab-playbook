#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def slugify_stem(path: Path) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in path.stem).strip("-")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def render_pdf_first_page(path: Path, tmpdir: Path, dpi: int) -> Path:
    out_prefix = tmpdir / path.stem
    run(["pdftoppm", "-png", "-r", str(dpi), "-singlefile", str(path), str(out_prefix)])
    return out_prefix.with_suffix(".png")


def optimize_with_cwebp(src: Path, dest: Path, width: int, quality: int) -> bool:
    cwebp = shutil.which("cwebp")
    if not cwebp:
        return False
    cmd = [cwebp, "-quiet", "-q", str(quality)]
    if width > 0:
        cmd.extend(["-resize", str(width), "0"])
    cmd.extend([str(src), "-o", str(dest)])
    run(cmd)
    return True


def optimize_with_pillow(src: Path, dest: Path, width: int, quality: int) -> None:
    from PIL import Image

    with Image.open(src) as image:
        image = image.convert("RGB")
        if width > 0 and image.width > width:
            height = round(image.height * width / image.width)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        image.save(dest, "WEBP", quality=quality, method=6)


def data_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/webp;base64,{encoded}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimize paper figures to WebP and optionally emit data URIs."
    )
    parser.add_argument("images", nargs="+", help="Image/PDF paths to optimize.")
    parser.add_argument("--out-dir", required=True, help="Output directory for WebP files.")
    parser.add_argument("--width", type=int, default=1600, help="Max output width; 0 disables resize.")
    parser.add_argument("--quality", type=int, default=82, help="WebP quality.")
    parser.add_argument("--pdf-dpi", type=int, default=180, help="DPI for first-page PDF render.")
    parser.add_argument("--data-uri-json", help="Optional JSON file containing data URIs.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, dict[str, str | int]] = {}
    with tempfile.TemporaryDirectory(prefix="paper2html-img-") as tmp:
        tmpdir = Path(tmp)
        for raw in args.images:
            src = Path(raw).expanduser().resolve()
            if not src.exists():
                raise SystemExit(f"Missing image: {src}")
            render_src = src
            if src.suffix.lower() == ".pdf":
                render_src = render_pdf_first_page(src, tmpdir, args.pdf_dpi)

            key = slugify_stem(src)
            dest = out_dir / f"{key}.webp"
            if not optimize_with_cwebp(render_src, dest, args.width, args.quality):
                optimize_with_pillow(render_src, dest, args.width, args.quality)

            manifest[key] = {
                "source": str(src),
                "webp": str(dest),
                "bytes": dest.stat().st_size,
            }

    if args.data_uri_json:
        for key, item in manifest.items():
            item["data_uri"] = data_uri(Path(str(item["webp"])))
        out = Path(args.data_uri_json).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(out)

    for key, item in manifest.items():
        print(f"{key}\t{item['bytes']}\t{item['webp']}")


if __name__ == "__main__":
    main()
