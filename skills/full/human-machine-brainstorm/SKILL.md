---
name: Human-Machine Brainstorm (人机风暴)
description: This skill should be used when the user asks to "人机风暴", "Human-Machine Brainstorm", "human storm", "ccb brainstorm", "需求对齐调度", "spec convergence", or wants a CCB-based multi-model requirement alignment loop with Codex as the dispatcher.
version: 0.1.0
disable-model-invocation: true
---

# Human-Machine Brainstorm (HMB) — CCB Dispatcher Loop

## Purpose

Run a repeatable multi-model requirement alignment loop in **CCB** where:
- **Codex** acts as the *dispatcher* (facilitator + router).
- **Claude Code** acts as the *scribe* (single source of truth spec author).
- **OpenCode (Gemini)** acts as the *divergent thinker* (alternatives + ASCII prototypes).

Keep every round auditable by exporting per-provider context into `./.ccb/history/` and keeping the canonical spec in `./.ccb/spec/`.

## Hard Rules

- Treat `./.ccb/spec/overview.md` as the **single source of truth**. Only Claude Code edits it.
- Never assume panes “share context”. Always broadcast updates explicitly.
- Enforce question IDs in this format:
  - Claude: `C-Q01`, `C-Q02`, ...
  - OpenCode: `O-Q01`, `O-Q02`, ...
- Accept user answers only in ID-addressed form (so routing is deterministic).

## Quick Start (zero-friction, recommended)

This workflow is optimized for a **2×Codex** setup:
- **Cmd pane** runs a dedicated **Codex Chair** (dispatcher).
- The normal **Codex provider pane** participates as a reviewer/solver (not just idle).

1) Create (or choose) a topic directory (recommended location: `$HOME/ccb-startups/...`).
   - Optional helper: `bash $HOME/.codex/skills/human-machine-brainstorm/scripts/hmb-init.sh "<topic-slug>"`

2) Start CCB.
   - If CCB global config enables the chair cmd pane, just run: `ccb`
   - Otherwise: `ccb claude codex opencode cmd` (fallback)

3) Talk only to the **Codex Chair** (cmd pane).
   - Paste the raw requirement.
   - The chair broadcasts to `claude`, `opencode`, and participant `codex` via `ask`.
   - Use the round prompt template in `references/round_prompt_template.md` if needed.

## Round Loop (R1/R2/R3...)

### Step A — Broadcast (dispatcher = Codex Chair)

Send the same “Round prompt” to:
- `ask claude "<ROUND PROMPT>"`
- `ask opencode "<ROUND PROMPT>"`
- `ask codex "<ROUND PROMPT>"` (participant Codex pane)

Require them to respond with:
- 10–20 numbered questions using `C-Q##` / `O-Q##` / `P-Q##`
- 1 ASCII diagram (flow/state/component)
- 1 short “current assumptions” list

### Step B — Collect Answers (human)

Ask the human to answer in this format:

- `C-Q01: ...`
- `C-Q02: ...`
- `O-Q01: ...`
- `P-Q01: ...`

Optionally allow a shared block:
- `SHARED: ...` (facts that apply to both)

### Step C — Route Answers (dispatcher = Codex)

Send Claude only `C-*` + `SHARED`.
Send OpenCode only `O-*` + `SHARED`.
Send participant Codex only `P-*` + `SHARED`.

### Step D — Export Evidence (end of round)

From the `cmd` pane (or any shell pane) run:
- `./.ccb/bin/round-save.sh 20`

This writes:
- `./.ccb/history/claude-<timestamp>.md`
- `./.ccb/history/codex-<timestamp>.md`
- `./.ccb/history/opencode-<timestamp>.md`

### Step E — Update Spec (scribe = Claude Code)

Ask Claude to update:
- `./.ccb/spec/overview.md` (bump version vN)
- `./.ccb/spec/open_questions.md` (close answered questions)
- `./.ccb/spec/decisions.md` (record non-reversible decisions)
- `./.ccb/spec/changelog.md` (vN → vN+1 diff)

Then re-run another round until all reviewers say “no blocking issues”.

## Final Handoff to GPT-5.2 (new session)

Provide a clean handoff pack:
- `./.ccb/spec/overview.md`
- `./.ccb/spec/decisions.md`
- `./.ccb/spec/open_questions.md` (should be empty or non-blocking)
- `./.ccb/spec/changelog.md`

Instruct GPT-5.2 to:
- Treat the spec as authoritative
- Output an executable plan first
- Use multi-agent decomposition for implementation/testing/review
