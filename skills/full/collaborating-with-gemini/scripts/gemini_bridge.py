#!/usr/bin/env python3
"""
Gemini Bridge Script for Codex Skills.

Wraps the Gemini CLI to provide a JSON-based interface and multi-turn sessions via SESSION_ID.
"""

import argparse
import json
import os
import queue
import shutil
import subprocess
import threading
import time
from pathlib import Path
from typing import List, Optional, Tuple


def run_shell_command(cmd: List[str], cwd: Optional[str] = None) -> Tuple[List[str], List[str], int]:
    """Execute a command and return stdout/stderr as lists of lines."""
    popen_cmd = cmd.copy()
    gemini_path = shutil.which("gemini") or cmd[0]
    popen_cmd[0] = gemini_path

    process = subprocess.Popen(
        popen_cmd,
        shell=False,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding="utf-8",
        cwd=cwd,
    )

    output_queue: "queue.Queue[Optional[str]]" = queue.Queue()
    GRACEFUL_SHUTDOWN_DELAY = 0.3
    stdout_lines: List[str] = []
    stderr_lines: List[str] = []

    def is_turn_completed(line: str) -> bool:
        try:
            data = json.loads(line)
            return data.get("type") == "turn.completed"
        except (json.JSONDecodeError, AttributeError, TypeError):
            return False

    def read_output() -> None:
        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                stripped = line.strip()
                output_queue.put(stripped)
                if is_turn_completed(stripped):
                    time.sleep(GRACEFUL_SHUTDOWN_DELAY)
                    process.terminate()
                    break
            process.stdout.close()
        output_queue.put(None)

    def read_stderr() -> None:
        if process.stderr:
            for line in iter(process.stderr.readline, ""):
                stderr_lines.append(line.rstrip("\n"))
            process.stderr.close()

    stdout_thread = threading.Thread(target=read_output)
    stderr_thread = threading.Thread(target=read_stderr)
    stdout_thread.start()
    stderr_thread.start()

    while True:
        try:
            line = output_queue.get(timeout=0.5)
            if line is None:
                break
            stdout_lines.append(line)
        except queue.Empty:
            if process.poll() is not None and not stdout_thread.is_alive():
                break

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
    stdout_thread.join(timeout=5)
    stderr_thread.join(timeout=5)

    while not output_queue.empty():
        try:
            line = output_queue.get_nowait()
            if line is not None:
                stdout_lines.append(line)
        except queue.Empty:
            break

    return stdout_lines, stderr_lines, process.returncode or 0


def windows_escape(prompt: str) -> str:
    """Windows style string escaping."""
    result = prompt.replace("\\", "\\\\")
    result = result.replace('"', '\\"')
    result = result.replace("\n", "\\n")
    result = result.replace("\r", "\\r")
    result = result.replace("\t", "\\t")
    result = result.replace("\b", "\\b")
    result = result.replace("\f", "\\f")
    result = result.replace("'", "\\'")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Gemini Bridge")
    parser.add_argument("--PROMPT", required=True, help="Instruction for the task to send to gemini.")
    parser.add_argument("--cd", required=True, type=Path, help="Set the workspace root for gemini before executing the task.")
    parser.add_argument("--sandbox", action="store_true", default=False, help="Run in sandbox mode. Defaults to `False`.")
    parser.add_argument(
        "--SESSION_ID",
        default="",
        help="Resume the specified session of gemini. Defaults to empty string (start a new session).",
    )
    parser.add_argument(
        "--return-all-messages",
        action="store_true",
        help="Return all messages (e.g. tool calls, traces) from the gemini session. By default only returns the assistant message text.",
    )
    parser.add_argument("--model", default="", help="Override the Gemini model.")

    args = parser.parse_args()

    if shutil.which("gemini") is None:
        result = {
            "success": False,
            "error": "Gemini CLI not found in PATH. Install it and ensure `gemini` is available before using this skill.",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    cd: Path = args.cd
    if not cd.exists():
        result = {
            "success": False,
            "error": f"The workspace root directory `{cd.absolute().as_posix()}` does not exist. Please check the path and try again.",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    prompt = args.PROMPT

    # Prefer positional prompt (the flag form has been deprecated in newer gemini-cli versions).
    cmd = ["gemini", "-o", "stream-json"]

    if args.sandbox:
        cmd.extend(["--sandbox"])

    if args.model:
        cmd.extend(["--model", args.model])

    if args.SESSION_ID:
        cmd.extend(["--resume", args.SESSION_ID])

    cmd.append(prompt)

    all_messages = []
    agent_messages = ""
    success = True
    err_message = ""
    session_id = None

    stdout_lines, stderr_lines, returncode = run_shell_command(cmd, cwd=cd.absolute().as_posix())

    for line in stdout_lines:
        try:
            line_dict = json.loads(line.strip())
            all_messages.append(line_dict)

            item_type = line_dict.get("type", "")
            item_role = line_dict.get("role", "")

            if item_type == "message" and item_role == "assistant":
                agent_messages += line_dict.get("content", "")

            if line_dict.get("session_id") is not None:
                session_id = line_dict.get("session_id")

        except json.JSONDecodeError:
            err_message += "\n\n[json decode error] " + line
            continue
        except Exception as error:
            err_message += "\n\n[unexpected error] " + f"Unexpected error: {error}. Line: {line!r}"
            continue

    result = {}

    # Treat SIGTERM (-15 on Unix, 15 on Windows) as success since we terminate Gemini ourselves.
    success = returncode in (0, -15, 15)
    if not success and not err_message:
        err_message = f"Gemini CLI exited with non-zero status: {returncode}"

    if session_id is None:
        success = False
        err_message = "Failed to get `SESSION_ID` from the gemini session.\n\n" + err_message
    else:
        result["SESSION_ID"] = session_id

    stderr_text = "\n".join(stderr_lines).strip()
    if stderr_text:
        err_message = (err_message + "\n\n" if err_message else "") + "[stderr]\n" + stderr_text

    result["agent_messages"] = agent_messages
    if not success:
        result["error"] = err_message

    result["success"] = success

    if args.return_all_messages:
        result["all_messages"] = all_messages

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
