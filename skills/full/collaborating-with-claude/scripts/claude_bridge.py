#!/usr/bin/env python3
"""
Claude Code Bridge Script for Codex Skills.

Wraps the Claude Code CLI to provide a JSON-based interface and multi-turn sessions via SESSION_ID.
"""

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def read_output_lines(cmd: List[str], cwd: Optional[str] = None) -> Tuple[List[str], List[str], int]:
    """Execute a command and capture stdout/stderr as lists of lines."""
    popen_cmd = cmd.copy()
    claude_path = shutil.which("claude") or cmd[0]
    popen_cmd[0] = claude_path

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

    stdout, stderr = process.communicate()
    stdout_lines = stdout.splitlines() if stdout else []
    stderr_lines = stderr.splitlines() if stderr else []
    return stdout_lines, stderr_lines, process.returncode


def extract_text(value: Any) -> str:
    """Recursively extract text from a Claude Code JSON payload."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(extract_text(item) for item in value)
    if isinstance(value, dict):
        if isinstance(value.get("text"), str):
            return value["text"]
        if "content" in value:
            return extract_text(value["content"])
        if "delta" in value:
            return extract_text(value["delta"])
        if "message" in value:
            return extract_text(value["message"])
    return ""


def update_role(obj: Dict[str, Any], current_role: Optional[str]) -> Optional[str]:
    """Track the current message role for streaming output."""
    role = obj.get("role")
    if isinstance(role, str):
        return role
    message = obj.get("message")
    if isinstance(message, dict):
        role = message.get("role")
        if isinstance(role, str):
            return role
    return current_role


def parse_stream_json(lines: List[str]) -> Tuple[Optional[str], str, List[Dict[str, Any]], str]:
    """Parse stream-json output into session_id, agent_messages, all_messages, error."""
    all_messages: List[Dict[str, Any]] = []
    agent_messages = ""
    err_message = ""
    session_id: Optional[str] = None
    current_role: Optional[str] = None
    saw_delta = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        try:
            obj = json.loads(stripped)
            if isinstance(obj, dict):
                all_messages.append(obj)
                if obj.get("session_id"):
                    session_id = obj.get("session_id")

                current_role = update_role(obj, current_role)
                is_delta = "delta" in obj or str(obj.get("type", "")).endswith("_delta")
                if is_delta:
                    saw_delta = True

                if current_role == "assistant":
                    if is_delta or not saw_delta:
                        agent_messages += extract_text(obj)
        except json.JSONDecodeError:
            err_message += "\n\n[json decode error] " + stripped
            continue
        except Exception as error:
            err_message += "\n\n[unexpected error] " + f"Unexpected error: {error}. Line: {stripped!r}"
            continue

    return session_id, agent_messages, all_messages, err_message


def parse_json_output(lines: List[str]) -> Tuple[Optional[str], str, List[Dict[str, Any]], str]:
    """Parse json (non-stream) output into session_id, agent_messages, all_messages, error."""
    err_message = ""
    raw = "\n".join(lines).strip()
    if not raw:
        return None, "", [], "No output received from Claude Code."
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as error:
        return None, raw, [], f"Failed to parse JSON output: {error}"

    session_id = None
    if isinstance(obj, dict) and obj.get("session_id"):
        session_id = obj.get("session_id")

    agent_messages = extract_text(obj)
    all_messages = [obj] if isinstance(obj, dict) else []
    return session_id, agent_messages, all_messages, err_message


def main() -> None:
    parser = argparse.ArgumentParser(description="Claude Code Bridge")
    parser.add_argument("--PROMPT", required=True, help="Instruction for the task to send to claude.")
    parser.add_argument("--cd", required=True, type=Path, help="Set the workspace root for claude before executing the task.")
    session_group = parser.add_mutually_exclusive_group()
    session_group.add_argument("--SESSION_ID", default="", help="Resume the specified session of claude.")
    session_group.add_argument("--session-id", dest="session_id", default="", help="Use a specific session ID (UUID).")
    session_group.add_argument("--continue", dest="continue_session", action="store_true", help="Continue the most recent session.")
    parser.add_argument("--fork-session", action="store_true", help="Fork session when resuming/continuing.")
    parser.add_argument("--no-session-persistence", action="store_true", help="Disable session persistence (print mode only).")
    parser.add_argument("--model", default="", help="Model override (alias like 'sonnet'/'opus', or a full model name).")
    parser.add_argument("--fallback-model", default="", help="Fallback model when the default is overloaded.")
    parser.add_argument("--max-budget-usd", default="", help="Max USD budget for the call (print mode only).")
    parser.add_argument("--json-schema", default="", help="JSON schema for structured output validation.")
    parser.add_argument("--input-format", default="text", choices=["text", "stream-json"], help="Claude input format.")
    parser.add_argument("--add-dir", action="append", default=[], help="Add additional working directories.")
    parser.add_argument("--append-system-prompt", default="", help="Append text to the default system prompt.")
    parser.add_argument("--system-prompt", default="", help="Replace the system prompt for the session.")
    parser.add_argument("--allowed-tools", action="append", default=[], help="Tools to allow without prompting.")
    parser.add_argument("--disallowed-tools", action="append", default=[], help="Tools to remove from context.")
    parser.add_argument("--tools", default="", help="Comma/space-separated list of tools to enable.")
    parser.add_argument("--permission-mode", default="", help="Start in a specified permission mode.")
    parser.add_argument("--permission-prompt-tool", default="", help="MCP tool to handle permission prompts.")
    parser.add_argument("--mcp-config", action="append", default=[], help="Load MCP servers from JSON files or strings.")
    parser.add_argument("--strict-mcp-config", action="store_true", help="Only use MCP servers from --mcp-config.")
    parser.add_argument("--settings", action="append", default=[], help="Load settings from JSON files or strings.")
    parser.add_argument("--setting-sources", default="", help="Comma-separated list of setting sources.")
    parser.add_argument("--agent", default="", help="Agent name to use for the session.")
    parser.add_argument("--agents", default="", help="JSON defining custom agents.")
    parser.add_argument("--output-format", default="stream-json", choices=["text", "json", "stream-json"], help="Claude output format.")
    parser.add_argument("--include-partial-messages", action="store_true", help="Include partial streaming events.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose CLI output (required for stream-json).")
    parser.add_argument(
        "--return-all-messages",
        action="store_true",
        help="Return all messages (e.g. tool calls, traces) from the claude session.",
    )

    args = parser.parse_args()

    session_id_expected = args.output_format in ("json", "stream-json") and not args.no_session_persistence

    cd: Path = args.cd
    if not cd.exists():
        result = {
            "success": False,
            "error": f"The workspace root directory `{cd.absolute().as_posix()}` does not exist. Please check the path and try again.",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    cmd = ["claude", "--print", args.PROMPT, "--output-format", args.output_format, "--input-format", args.input_format]

    if args.include_partial_messages:
        cmd.append("--include-partial-messages")

    if args.output_format == "stream-json" and not args.verbose:
        cmd.append("--verbose")
    elif args.verbose:
        cmd.append("--verbose")

    if args.model:
        cmd.extend(["--model", args.model])

    if args.fallback_model:
        cmd.extend(["--fallback-model", args.fallback_model])

    if args.max_budget_usd:
        cmd.extend(["--max-budget-usd", args.max_budget_usd])

    if args.json_schema:
        cmd.extend(["--json-schema", args.json_schema])

    if args.continue_session:
        cmd.append("--continue")

    if args.SESSION_ID:
        cmd.extend(["--resume", args.SESSION_ID])

    if args.session_id:
        cmd.extend(["--session-id", args.session_id])

    if args.fork_session:
        cmd.append("--fork-session")

    if args.no_session_persistence:
        cmd.append("--no-session-persistence")

    for extra_dir in args.add_dir:
        cmd.extend(["--add-dir", extra_dir])

    if args.system_prompt:
        cmd.extend(["--system-prompt", args.system_prompt])

    if args.append_system_prompt:
        cmd.extend(["--append-system-prompt", args.append_system_prompt])

    for tool in args.allowed_tools:
        cmd.extend(["--allowedTools", tool])

    if args.tools:
        cmd.extend(["--tools", args.tools])

    for tool in args.disallowed_tools:
        cmd.extend(["--disallowedTools", tool])

    if args.permission_mode:
        cmd.extend(["--permission-mode", args.permission_mode])

    if args.permission_prompt_tool:
        cmd.extend(["--permission-prompt-tool", args.permission_prompt_tool])

    for cfg in args.mcp_config:
        cmd.extend(["--mcp-config", cfg])

    if args.strict_mcp_config:
        cmd.append("--strict-mcp-config")

    for settings in args.settings:
        cmd.extend(["--settings", settings])

    if args.setting_sources:
        cmd.extend(["--setting-sources", args.setting_sources])

    if args.agent:
        cmd.extend(["--agent", args.agent])

    if args.agents:
        cmd.extend(["--agents", args.agents])

    stdout_lines, stderr_lines, returncode = read_output_lines(cmd, cwd=cd.absolute().as_posix())

    if args.output_format == "stream-json":
        session_id, agent_messages, all_messages, err_message = parse_stream_json(stdout_lines)
    elif args.output_format == "json":
        session_id, agent_messages, all_messages, err_message = parse_json_output(stdout_lines)
    else:
        session_id = args.SESSION_ID or args.session_id or None
        agent_messages = "\n".join(stdout_lines).strip()
        all_messages = []
        err_message = ""

    success = returncode == 0
    if not success and not err_message:
        err_message = f"Claude Code exited with non-zero status: {returncode}"
    if session_id is None and session_id_expected:
        success = False
        err_message = "Failed to get `SESSION_ID` from the claude session.\n\n" + err_message

    stderr_text = "\n".join(stderr_lines).strip()
    if stderr_text:
        err_message = (err_message + "\n\n" if err_message else "") + "[stderr]\n" + stderr_text

    result: Dict[str, Any] = {"success": success}
    if session_id is not None:
        result["SESSION_ID"] = session_id
    result["agent_messages"] = agent_messages
    if success:
        pass
    else:
        result["error"] = err_message

    if args.return_all_messages:
        result["all_messages"] = all_messages

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
