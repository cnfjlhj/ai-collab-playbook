# Module: LaTeX Rhythm Refiner (Post-Process) — Feature-Parity Import

This module preserves the distinctive “rhythm refinement” rules and constraints from the legacy `latex-rhythm-refiner` skill.

## When to Use (Must Support)

- After content generation is complete.
- When prose flow feels monotonous/blocky.

## When NOT to Use (Must Support)

- During initial drafting.
- For citation verification/addition.
- For technical/structural LaTeX fixes.

## Core Principles (Hard Constraints)

1) Preserve citations exactly
   - Every `\\cite{...}` must remain in place.
   - Do not add/remove/relocate citations.
   - Do not attach a citation to a different claim.
2) Vary rhythm stochastically
   - Mix short/medium/long sentences; avoid long runs of similar length.
   - Vary paragraph length across adjacent paragraphs.
3) Remove fillers
   - Replace “in order to” → “to”, etc.
4) Minimize transitions
   - Remove “Moreover/However/Therefore” when structure already implies the relation.
5) Tighten prose
   - Prefer concrete verbs; avoid hedge stacks; ensure each paragraph has one main idea.

## Processing Workflow (Must Support)

Per section:
1) Read section for intent.
2) Identify all citation locations and their attached claims.
3) Map sentence/paragraph rhythm.
4) Refine: break/combine sentences, adjust paragraph boundaries, strip filler.
5) Verify citations remain semantically attached.
6) Output refined LaTeX.

## Verification Checklist (Must Support)

- [ ] Citation count unchanged
- [ ] Citation keys unchanged
- [ ] Each citation still supports the same claim
- [ ] No 3+ consecutive sentences of similar length
- [ ] Paragraph length variety improved
- [ ] Filler phrases removed
- [ ] Unnecessary transitions removed
- [ ] No LaTeX structure/command breakage

## Notes on “No-Omission” Parity

If the user asks for the original phrasing/rules, consult:
- `~/.codex/skills/latex-rhythm-refiner/SKILL.md`

