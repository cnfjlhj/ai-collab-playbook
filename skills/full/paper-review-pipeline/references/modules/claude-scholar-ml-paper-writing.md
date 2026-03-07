# Module: Claude-Scholar ML Paper Writing (Extended Workflow) — Feature-Parity Import

This module preserves the distinctive *extended* workflows from the legacy `claude-scholar-ml-paper-writing` skill that are not strictly required for the core paper-review pipeline, but must remain available for parity.

## Distinctive Features to Preserve

### 1) Proactive drafting posture (Must Support)

- When the repo/results are clear, produce concrete drafts rather than blocking on questions.
- When uncertain, draft with flagged uncertainties rather than waiting.

### 2) “Never hallucinate citations” rule (Must Support)

- Never fabricate BibTeX or references.
- If a citation cannot be verified, mark as placeholder and inform the user.

This must remain consistent with pipeline guardrails.

### 3) Literature research & paper discovery workflow (Must Support)

Maintain a systematic discovery flow:
1) Define search scope and keywords.
2) Search arXiv and other academic databases.
3) Screen by title/abstract.
4) Evaluate paper quality with a multi-dimension rubric.
5) Select and extract citations.
6) Verify citations programmatically / via reliable metadata sources.

### 4) Paper quality evaluation rubric (Must Support)

Preserve a weighted quality rubric (example dimensions):
- Innovation
- Method completeness (reproducibility)
- Experimental thoroughness
- Writing quality
- Relevance/impact

### 5) Related work positioning guidance (Must Support)

- Prefer synthesis and positioning over enumerating papers.
- Use citations to support claims about “what prior work does”.

## Notes on “No-Omission” Parity

The legacy skill includes additional detailed references for literature research. When the user requests those details, consult:
- `~/.codex/skills/claude-scholar-ml-paper-writing/SKILL.md`

(The skill may be disabled for auto-invocation, but its content remains available for reference.)

