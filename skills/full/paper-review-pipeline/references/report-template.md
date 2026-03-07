# Report Template (paper-review-pipeline)

This template is the required structure for outputs produced by this skill.

## Header

- Paper context: venue (ICML/ICLR/NeurIPS/AAAI), submission stage (draft/blind/camera-ready), scope (full paper vs sections).
- Inputs received: LaTeX excerpt / PDF / reviewer comments / bibliography presence.
- Mode: `targeted` or `full-parallel`.

## Tracks (Full-Parallel Only)

If mode is `full-parallel`, include all sections below and keep them visible:

### Track A — Paper Self-Review

- Structure review findings
- Logic consistency findings
- Figures/tables findings
- Writing clarity findings
- Final checklist (checked/unchecked)

### Track B — Academic Paper Helper

- Paste-ready fixes (at least 2 blocks if issues exist)
- LaTeX pitfalls (if relevant)
- Suggested structural templates (if requested)

### Track C — ML Paper Writing (Narrative + Reviewer Attacks)

- One-sentence contribution (as understood; ask for confirmation if needed)
- What/Why/So-what assessment
- Top-5 likely reviewer attacks + defense text suggestions

### Track D — Anti-AI Polish

- Pattern detections (>= 3 types if issues exist)
- Revised version(s)
- Optional quick scoring (if user wants)

### Track E — LaTeX Rhythm Refinement

- Targeted rewrites (1–3)
- Verification checklist (citations/LaTeX preserved)

### Track F — Citation Audit (Claim-level)

- `SKIP` (with reason + required inputs) OR legacy-style audit report

### Track G — Rebuttal / Review Response

- If reviewer comments exist: classification + strategy + rebuttal draft + revision plan
- Else: rebuttal readiness pack (predicted comments + strategy + where-to-point)

## Final Synthesis (Always)

### View A — Section-by-Section Review (Consolidated)

For each section:
- What works (1–3 bullets)
- Missing/unclear (P0/P1/P2 tagged)
- Concrete fixes (paste-ready when feasible)

### View B — P0/P1/P2 Issue List (Consolidated)

Each issue must include:
- Priority: P0/P1/P2
- Category
- Where (section + anchor)
- Problem
- Fix
- Verification (if needed)

### Minimal Revision Plan (3–8 items)

- Task → acceptance criteria → dependency notes

### Conflicts & Resolutions

- Track disagreements (if any) + the adopted resolution and rationale

