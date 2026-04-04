#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from string import Template


def read_template(path: Path) -> Template:
    return Template(path.read_text(encoding="utf-8"))


def render_template(path: Path, context: dict[str, str]) -> str:
    return read_template(path).safe_substitute(context)


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists (use --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def ensure_writable(paths: list[Path], force: bool) -> None:
    if force:
        return
    conflicts = [path for path in paths if path.exists()]
    if conflicts:
        joined = "\n".join(str(path) for path in conflicts)
        raise FileExistsError(
            "Refusing to partially initialize an existing workspace. "
            "Conflicting files:\n"
            f"{joined}\n"
            "Use --force to overwrite the generated files."
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize a workspace for the research-lead-sidecar workflow.",
    )
    parser.add_argument("root", help="Target workspace directory")
    parser.add_argument("--topic", required=True, help="Short task topic")
    parser.add_argument("--goal", required=True, help="Concrete deliverable or decision")
    parser.add_argument(
        "--mode",
        default="coupled",
        choices=("research", "coupled", "implementation"),
        help="Primary task mode",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files if they already exist",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    skill_dir = Path(__file__).resolve().parents[1]
    assets_dir = skill_dir / "assets"
    references_dir = skill_dir / "references"

    today = dt.date.today().isoformat()
    context = {
        "date": today,
        "topic": args.topic,
        "goal": args.goal,
        "mode": args.mode,
        "topic_yaml": json.dumps(args.topic, ensure_ascii=False),
        "goal_yaml": json.dumps(args.goal, ensure_ascii=False),
        "mode_yaml": json.dumps(args.mode, ensure_ascii=False),
    }

    root.mkdir(parents=True, exist_ok=True)
    (root / "handoffs").mkdir(parents=True, exist_ok=True)
    (root / "artifacts").mkdir(parents=True, exist_ok=True)

    generated = {
        root / "research-state.yaml": render_template(
            assets_dir / "research-state.yaml.tpl",
            context,
        ),
        root / "findings.md": render_template(assets_dir / "findings.md.tpl", context),
        root / "progress.md": render_template(assets_dir / "progress.md.tpl", context),
        root / "handoffs" / "worker-handoff-template.md": (
            references_dir / "worker-handoff-template.md"
        ).read_text(encoding="utf-8"),
    }

    ensure_writable(list(generated.keys()), force=args.force)

    for path, content in generated.items():
        write_file(path, content, force=args.force)

    print(root)
    for path in generated:
        print(path.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
