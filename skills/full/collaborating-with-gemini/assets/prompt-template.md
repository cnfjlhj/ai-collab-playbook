# Gemini Prompt Template (Token-Efficient)

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

## Image Analysis (screenshot in workspace)

```
Task:
- Analyze the UI screenshot at `.codex_uploads/<filename>.png`.

Constraints:
- Describe what you see, then answer: <specific question>.
- Keep observations concise.

Output:
- Bullet list of observations and recommendations.
```
