# Workspace Files

Initialize the workspace when the task will span multiple milestones, more than one sidecar, or more than one session.

## Expected Layout

```text
<task-root>/
├── artifacts/
├── research-state.yaml
├── findings.md
├── progress.md
└── handoffs/
    └── worker-handoff-template.md
```

## File Rules

### `research-state.yaml`

Use for the **current accepted state** only:
- current focus
- critical path
- active sidecars
- accepted direction
- next merge checkpoint

Do not turn this into a diary. Rewrite it when the plan changes.

### `findings.md`

Use for evidence-backed items the lead has accepted:
- facts
- comparisons
- decisions
- unresolved but well-formed questions

Do not dump raw sidecar notes here before the lead checks them.

### `progress.md`

Use as the brief chronological log:
- milestone reached
- delegation decision
- retry reason
- blocker
- plan change

Keep entries short and operational.

### `handoffs/worker-handoff-template.md`

Use this as the fixed contract for all sidecars. If a sidecar returns in another format, normalize it before merging.

### `artifacts/`

Use this for sidecar return payloads that are too bulky for `findings.md` or `progress.md`:
- tables
- logs
- exported diffs
- screenshots
- raw experiment summaries

## Update Cadence

Update:
- `research-state.yaml` after each milestone or direction change
- `findings.md` when new evidence is accepted
- `progress.md` after each milestone, retry, or delegation decision

If the task is short and finishes inside one milestone, you can skip the workspace entirely.
