---
name: collaborating-with-codex
description: Use when you explicitly want a second local or SSH remote Codex CLI session to prototype, debug, or review code, while your current session remains the primary owner of the final result.
---

## Quick Start

```bash
python scripts/codex_bridge.py --cd "/path/to/project" --PROMPT "Your task"
```

Remote Codex over SSH:

```bash
python scripts/codex_bridge.py --ssh "server-alias" --cd "/remote/project" --PROMPT "Your task"
```

**Output:** JSON with `success`, `SESSION_ID`, `agent_messages`, and optional `error`.

## Parameters

```
usage: codex_bridge.py [-h] --PROMPT PROMPT --cd CD [--sandbox {read-only,workspace-write,danger-full-access}] [--SESSION_ID SESSION_ID] [--skip-git-repo-check]
                       [--return-all-messages] [--image IMAGE] [--model MODEL] [--yolo] [--profile PROFILE] [--ssh SSH] [--ssh-option SSH_OPTION]
                       [--codex-bin CODEX_BIN]

Codex Bridge

options:
  -h, --help            show this help message and exit
  --PROMPT PROMPT       Instruction for the task to send to codex.
  --cd CD               Set the workspace root for codex before executing the task.
  --sandbox {read-only,workspace-write,danger-full-access}
                        Sandbox policy for model-generated commands. Defaults to `read-only`.
  --SESSION_ID SESSION_ID
                        Resume the specified session of the codex. Defaults to `None`, start a new session.
  --skip-git-repo-check
                        Allow codex running outside a Git repository (useful for one-off directories).
  --return-all-messages
                        Return all messages (e.g. reasoning, tool calls, etc.) from the codex session. Set to `False` by default, only the agent's final reply message is
                        returned.
  --image IMAGE         Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag.
  --model MODEL         The model to use for the codex session. This parameter is strictly prohibited unless explicitly specified by the user.
  --yolo                Run every command without approvals or sandboxing. Only use when `sandbox` couldn't be applied.
  --profile PROFILE     Configuration profile name to load from `~/.codex/config.toml`. This parameter is strictly prohibited unless explicitly specified by the user.
  --ssh SSH             Run Codex on a remote host via SSH. Value can be an SSH alias or user@host. When set, --cd and --image paths are remote paths.
  --ssh-option SSH_OPTION
                        Extra ssh option, repeatable. Example: --ssh-option=-J --ssh-option=bastion
  --codex-bin CODEX_BIN
                        Codex executable to run locally or on the remote host. Defaults to `codex`. `--remote-codex` is accepted as a backward-compatible alias.
```

## Multi-turn Sessions

**Always capture `SESSION_ID`** from the first response for follow-up:

```bash
# Initial task
python scripts/codex_bridge.py --cd "/project" --PROMPT "Analyze auth in login.py"

# Continue with SESSION_ID
python scripts/codex_bridge.py --cd "/project" --SESSION_ID "uuid-from-response" --PROMPT "Write unit tests for that"
```

Remote sessions use the same `SESSION_ID`, but continue them against the same SSH host:

```bash
python scripts/codex_bridge.py --ssh "server-alias" --cd "/remote/project" --SESSION_ID "uuid-from-response" --PROMPT "Now implement it"
```

## SSH Remote Codex

Use `--ssh` when the repository, runtime, or credentials needed for the task live on a remote server.

Requirements:
- Local machine can run `ssh <host>` non-interactively.
- Remote host has `codex` installed and available in the remote non-interactive shell `PATH`, or pass `--codex-bin "/absolute/path/to/codex"`.
- The remote host should use a POSIX-compatible shell for command quoting.
- `--cd` is a remote absolute path when `--ssh` is set.
- `--image` paths are also remote paths when `--ssh` is set. Upload local images first if Codex on the server needs them.

Examples:

```bash
# Use an SSH config alias
python scripts/codex_bridge.py --ssh "gpu-box" --cd "/srv/app" --PROMPT "Review this service for race conditions"

# Use user@host and a remote codex path
python scripts/codex_bridge.py --ssh "ubuntu@example.com" --codex-bin "/home/ubuntu/.local/bin/codex" --cd "/home/ubuntu/app" --PROMPT "Run the failing tests and diagnose"

# Use a jump host
python scripts/codex_bridge.py --ssh "private-box" --ssh-option=-J --ssh-option=bastion --cd "/workspace/repo" --PROMPT "Inspect the deployment scripts"
```

Do not use `--ssh` for local repositories. Do not pass `--model` or `--profile` unless the user explicitly requested them.

## Common Patterns

**Prototyping (read-only, request diffs):**
```bash
python scripts/codex_bridge.py --cd "/project" --PROMPT "Generate unified diff to add logging"
```

**Debug with full trace:**
```bash
python scripts/codex_bridge.py --cd "/project" --PROMPT "Debug this error" --return-all-messages
```

**Remote debug with write access:**
```bash
python scripts/codex_bridge.py --ssh "server-alias" --cd "/remote/project" --sandbox workspace-write --PROMPT "Fix the failing integration test and summarize the patch"
```
