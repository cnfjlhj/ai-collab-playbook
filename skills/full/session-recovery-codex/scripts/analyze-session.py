#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


NOISE_PREFIXES = (
    "# AGENTS.md instructions",
    "<environment_context>",
    "<INSTRUCTIONS>",
    "<subagent_notification>",
)


def _as_path(p: str) -> Path:
    return Path(os.path.expanduser(p)).resolve()


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


def _find_session_file_by_id(sessions_root: Path, session_id: str, max_files: int = 2000) -> Optional[Path]:
    files = _iter_session_files(sessions_root)
    scanned = 0
    for path in files:
        scanned += 1
        if scanned > max_files:
            break
        meta = _load_session_meta(path)
        if not meta:
            continue
        if str(meta.get("id") or "") == session_id:
            return path
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


def _maybe_parse_json(s: str) -> Optional[Any]:
    try:
        return json.loads(s)
    except Exception:
        return None


def _extract_changed_files(text: str) -> list[str]:
    changed: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.match(r"^[AMDR]\s+", line):
            candidate = line[2:].strip()
            # Best-effort filter to avoid false positives (e.g., "C = 3.5" constants).
            if candidate.startswith(("/", "~", "./", "../")) or ("/" in candidate) or ("." in candidate):
                changed.append(candidate)
    return changed


@dataclass
class PlanStep:
    step: str
    status: str


@dataclass
class Analysis:
    session_id: str
    start_time: str
    cwd: str
    file: str
    last_user_request: str
    last_messages: list[tuple[str, str]]
    open_steps: list[PlanStep]
    changed_files: list[str]
    key_assistant_excerpt: str


def _analyze_session_file(path: Path) -> Analysis:
    meta = _load_session_meta(path) or {}
    session_id = str(meta.get("id") or "")
    start_time = str(meta.get("timestamp") or "")
    cwd = str(meta.get("cwd") or "")

    last_messages: deque[tuple[str, str]] = deque(maxlen=6)
    last_meaningful_user_text = ""
    last_assistant_text = ""
    last_plan: list[PlanStep] = []
    changed_files: set[str] = set()

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

                typ = obj.get("type")
                payload = obj.get("payload") or {}

                if typ == "response_item":
                    item_type = payload.get("type")
                    if item_type == "message":
                        role = payload.get("role")
                        if role in ("user", "assistant"):
                            text = _extract_message_text(payload)
                            if text:
                                last_messages.append((role, _truncate(text, 220)))
                            if role == "user" and text and not _is_noise_user_text(text):
                                last_meaningful_user_text = text
                            if role == "assistant" and text:
                                last_assistant_text = text

                    elif item_type == "function_call":
                        name = payload.get("name")
                        if name == "update_plan":
                            args_raw = payload.get("arguments")
                            if isinstance(args_raw, str):
                                args_obj = _maybe_parse_json(args_raw)
                                if isinstance(args_obj, dict):
                                    plan = args_obj.get("plan")
                                    if isinstance(plan, list):
                                        parsed: list[PlanStep] = []
                                        for p in plan:
                                            if not isinstance(p, dict):
                                                continue
                                            step = p.get("step")
                                            status = p.get("status")
                                            if isinstance(step, str) and isinstance(status, str):
                                                parsed.append(PlanStep(step=step, status=status))
                                        if parsed:
                                            last_plan = parsed

                    elif item_type in ("function_call_output", "custom_tool_call_output"):
                        out = payload.get("output")
                        text_out = ""
                        if isinstance(out, str):
                            if item_type == "custom_tool_call_output":
                                # payload.output is usually a JSON blob: {"output": "...", "metadata": {...}}
                                out_obj = _maybe_parse_json(out)
                                if isinstance(out_obj, dict) and isinstance(out_obj.get("output"), str):
                                    text_out = out_obj["output"]
                                else:
                                    text_out = out
                            else:
                                text_out = out
                        if text_out:
                            for fp in _extract_changed_files(text_out):
                                changed_files.add(fp)

    except OSError:
        pass

    last_user_request = last_meaningful_user_text.strip() or ""
    key_excerpt = last_assistant_text.strip() or ""

    open_steps: list[PlanStep] = []
    for s in last_plan:
        if s.status != "completed":
            open_steps.append(s)

    return Analysis(
        session_id=session_id,
        start_time=start_time,
        cwd=cwd,
        file=str(path),
        last_user_request=_truncate(last_user_request, 1200) if last_user_request else "",
        last_messages=list(last_messages),
        open_steps=open_steps,
        changed_files=sorted(changed_files),
        key_assistant_excerpt=_truncate(key_excerpt, 1200) if key_excerpt else "",
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Analyze a Codex session by session id or file path.")
    parser.add_argument("--id", help="Session id (session_meta.payload.id).")
    parser.add_argument("--file", help="Path to a session .jsonl file.")
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", "~/.codex"), help="Codex home (default: $CODEX_HOME or ~/.codex).")
    args = parser.parse_args(argv)

    if not args.id and not args.file:
        print("Provide --id <session_id> or --file <path>", file=sys.stderr)
        return 2

    sessions_root = _as_path(args.codex_home) / "sessions"
    target: Optional[Path] = None
    if args.file:
        target = _as_path(args.file)
        if not target.exists():
            print(f"Session file not found: {target}", file=sys.stderr)
            return 2
    else:
        target = _find_session_file_by_id(sessions_root, args.id)
        if not target:
            print(f"Session id not found under {sessions_root}: {args.id}", file=sys.stderr)
            return 2

    a = _analyze_session_file(target)

    print(f"Session: {a.session_id}")
    print(f"File: {a.file}")
    print(f"Start time: {a.start_time}")
    print(f"CWD: {a.cwd}")
    print()

    print("Last user request:")
    if a.last_user_request:
        print(a.last_user_request)
    else:
        print("(not found)")
    print()

    print("Open items (from latest update_plan, if present):")
    if a.open_steps:
        for s in a.open_steps:
            print(f"- [{s.status}] {s.step}")
    else:
        print("(no update_plan records found)")
    print()

    print("Files involved (best-effort from tool outputs):")
    if a.changed_files:
        for fp in a.changed_files:
            print(f"- {fp}")
    else:
        print("(not found)")
    print()

    print("Last messages:")
    if a.last_messages:
        for role, text in a.last_messages[-5:]:
            print(f"- {role}: {text}")
    else:
        print("(not found)")
    print()

    print("Key assistant excerpt:")
    if a.key_assistant_excerpt:
        print(a.key_assistant_excerpt)
    else:
        print("(not found)")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
