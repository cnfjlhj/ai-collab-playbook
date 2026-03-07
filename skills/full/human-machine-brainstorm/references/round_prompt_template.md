# HMB Round Prompt Template

Copy this template and fill in the placeholders, then send it via:
- `CCB_CALLER=codex ask claude "<...>"`
- `CCB_CALLER=codex ask opencode "<...>"`

---

## Context

- Topic: <topic>
- Current spec version: <vN or v0>
- Round: <R1/R2/...>
- Goal: <what this round must decide/clarify>

## Rules

1) Ask questions only. Do not write the final spec.
2) Use question IDs:
   - Claude: `C-Q01`, `C-Q02`, ...
   - OpenCode: `O-Q01`, `O-Q02`, ...
3) Ask 10–20 questions, sorted by priority (P0/P1/P2).
4) Include exactly 1 ASCII diagram (flow/state/component).
5) End with a short list: `Assumptions:` (max 7 bullets).

## Original Problem (raw)

<paste raw user idea here>

## Output Format

- Questions:
  - P0:
    - C-Q01: ...
    - C-Q02: ...
  - P1:
  - P2:
- ASCII Diagram:
  - ...
- Assumptions:
  - ...

