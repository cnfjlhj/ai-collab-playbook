# Claude Prompt Template (Token-Efficient)

Note: Prefer choosing models via CLI aliases (e.g., `--model sonnet` for routine work, `--model opus` for harder tasks) instead of hard-coding versioned model IDs. If you omit `--model`, Claude Code uses its configured default.

## Analysis / Plan (no code changes)

```
Task:
- <what to analyze>

Repo pointers:
- <file paths + approximate line numbers>

Constraints:
- Keep it concise and actionable.
- Do not paste large snippets; reference files/lines instead.

Output:
- Bullet list of findings and a proposed plan.
```

## Patch (Unified Diff only)

```
Task:
- <what to change>

Repo pointers:
- <file paths + approximate line numbers>

Constraints:
- OUTPUT: Unified Diff Patch ONLY.
- Strictly prohibit any actual modifications.
- Minimal, focused changes. No unrelated refactors.

Output:
- A single unified diff patch.
```

## Review (audit an existing diff)

```
Task:
- Review the following unified diff for correctness, edge cases, and missing tests.

Constraints:
- Return a checklist of issues + suggested fixes (no code unless requested).

Input diff:
<paste unified diff here>
```
