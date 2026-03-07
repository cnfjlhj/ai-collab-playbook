#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional


NOISE_PREFIXES = (
    "# AGENTS.md instructions",
    "<environment_context>",
    "<INSTRUCTIONS>",
    "<subagent_notification>",
)


def _as_path(p: str) -> Path:
    return Path(os.path.expanduser(p)).resolve()


def _find_project_root(cwd: Path) -> Path:
    cur = cwd.resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".git").exists():
            return parent
    return cur


def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _iter_session_files(sessions_root: Path) -> list[Path]:
    if not sessions_root.exists():
        return []
    return sorted(sessions_root.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)


def _read_first_json_obj(path: Path, max_lines: int = 20) -> Optional[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as f:
            for _ in range(max_lines):
                line = f.readline()
                if not line:
                    return None
                line = line.strip()
                if not line:
                    continue
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return None
    return None


def _load_session_meta(path: Path) -> Optional[dict[str, Any]]:
    first = _read_first_json_obj(path)
    if not first:
        return None
    if first.get("type") == "session_meta":
        return first.get("payload") or {}
    return None


def _extract_message_text(message_payload: dict[str, Any]) -> str:
    parts: list[str] = []
    for item in message_payload.get("content") or []:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            parts.append(text.strip())
    return "\n".join(parts).strip()


def _is_noise_user_text(text: str) -> bool:
    stripped = text.lstrip()
    return any(stripped.startswith(prefix) for prefix in NOISE_PREFIXES)


def _truncate(text: str, max_chars: int) -> str:
    t = " ".join(text.strip().split())
    if len(t) <= max_chars:
        return t
    return t[: max(0, max_chars - 1)] + "…"


@dataclass(frozen=True)
class SessionSummary:
    index: int
    session_id: str
    start_time: str
    cwd: str
    file: str
    user_messages: int
    assistant_messages: int
    topic: str
    last_messages: list[tuple[str, str]]


def _summarize_session(path: Path, meta: dict[str, Any], last_n: int = 3) -> SessionSummary:
    user_messages = 0
    assistant_messages = 0
    last_messages: deque[tuple[str, str]] = deque(maxlen=last_n)
    last_meaningful_user_text: str = ""

    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if obj.get("type") != "response_item":
                    continue
                payload = obj.get("payload") or {}
                if payload.get("type") != "message":
                    continue

                role = payload.get("role")
                if role not in ("user", "assistant"):
                    continue
                text = _extract_message_text(payload)
                if role == "user":
                    user_messages += 1
                    if text and not _is_noise_user_text(text):
                        last_meaningful_user_text = text
                else:
                    assistant_messages += 1

                if text:
                    last_messages.append((role, text))
    except OSError:
        pass

    session_id = str(meta.get("id") or "")
    start_time = str(meta.get("timestamp") or "")
    cwd = str(meta.get("cwd") or "")
    topic_source = last_meaningful_user_text or (last_messages[-1][1] if last_messages else "")
    topic = _truncate(topic_source, 80) if topic_source else ""

    return SessionSummary(
        index=0,
        session_id=session_id,
        start_time=start_time,
        cwd=cwd,
        file=str(path),
        user_messages=user_messages,
        assistant_messages=assistant_messages,
        topic=topic,
        last_messages=[(r, _truncate(t, 140)) for r, t in list(last_messages)],
    )


def _format_time(ts: str) -> str:
    if not ts:
        return ""
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return ts


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="List recent Codex sessions for the current project.")
    parser.add_argument("--cwd", default=os.getcwd(), help="Current working directory (default: pwd).")
    parser.add_argument("--limit", type=int, default=5, help="How many sessions to show (default: 5).")
    parser.add_argument("--max-files", type=int, default=60, help="Max recent session files to scan (default: 60).")
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", "~/.codex"), help="Codex home (default: $CODEX_HOME or ~/.codex).")
    parser.add_argument("--all", action="store_true", help="List sessions across all projects (ignore project filter).")
    args = parser.parse_args(argv)

    cwd = _as_path(args.cwd)
    project_root = _find_project_root(cwd)
    sessions_root = _as_path(args.codex_home) / "sessions"

    files = _iter_session_files(sessions_root)
    if not files:
        print(f"No sessions found under: {sessions_root}", file=sys.stderr)
        return 2

    summaries: list[SessionSummary] = []
    scanned = 0
    for path in files:
        if scanned >= args.max_files:
            break
        scanned += 1

        meta = _load_session_meta(path)
        if not meta:
            continue

        session_cwd = meta.get("cwd")
        if not args.all:
            if not isinstance(session_cwd, str) or not session_cwd:
                continue
            if not _is_relative_to(_as_path(session_cwd), project_root):
                continue

        summaries.append(_summarize_session(path, meta))
        if len(summaries) >= args.limit:
            break

    if not summaries:
        print(f"No sessions matched project root: {project_root}")
        return 0

    print(f"Project root: {project_root}")
    print(f"Sessions root: {sessions_root}")
    print()

    for i, s in enumerate(summaries, start=1):
        s = SessionSummary(
            index=i,
            session_id=s.session_id,
            start_time=s.start_time,
            cwd=s.cwd,
            file=s.file,
            user_messages=s.user_messages,
            assistant_messages=s.assistant_messages,
            topic=s.topic,
            last_messages=s.last_messages,
        )
        total = s.user_messages + s.assistant_messages
        print(f"{i}. id={s.session_id}  time={_format_time(s.start_time)}")
        print(f"   cwd={s.cwd}")
        print(f"   messages: user={s.user_messages} assistant={s.assistant_messages} total={total}")
        if s.topic:
            print(f"   topic: {s.topic}")
        print("   last:")
        if s.last_messages:
            for role, text in s.last_messages:
                print(f"     - {role}: {text}")
        else:
            print("     (no messages found)")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
