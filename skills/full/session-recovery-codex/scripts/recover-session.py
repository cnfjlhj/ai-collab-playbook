#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
LIST_SCRIPT = SKILL_ROOT / "scripts" / "list-sessions.py"
RESUME_SCRIPT = SKILL_ROOT.parent / "codex-resume" / "scripts" / "resume-session.py"


def run(args: list[str]) -> int:
    completed = subprocess.run(args)
    return completed.returncode


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Unified entrypoint for Codex session recovery."
    )
    parser.add_argument("--id", help="Codex session id to resume directly")
    parser.add_argument("--cwd", default=str(Path.cwd()), help="Working directory for repo-aware filtering")
    parser.add_argument("--limit", type=int, default=5, help="How many recent sessions to list when --id is absent")
    parser.add_argument("--full", action="store_true", help="Pass through to resume-session.py")
    parser.add_argument("--max-messages", type=int, help="Pass through to resume-session.py")
    parser.add_argument("--max-tool-outputs", type=int, help="Pass through to resume-session.py")
    parser.add_argument("--include-noise", action="store_true", help="Pass through to resume-session.py")
    args = parser.parse_args(argv)

    if args.id:
        command = [sys.executable, str(RESUME_SCRIPT), "--id", args.id, "--cwd", args.cwd]
        if args.full:
            command.append("--full")
        if args.max_messages is not None:
            command.extend(["--max-messages", str(args.max_messages)])
        if args.max_tool_outputs is not None:
            command.extend(["--max-tool-outputs", str(args.max_tool_outputs)])
        if args.include_noise:
            command.append("--include-noise")
        return run(command)

    command = [
        sys.executable,
        str(LIST_SCRIPT),
        "--cwd",
        args.cwd,
        "--limit",
        str(args.limit),
    ]
    return run(command)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
