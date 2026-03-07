# Full-Parallel Tracks Protocol (paper-review-pipeline)

This protocol defines a **comprehensive**, **track-by-track** paper review that preserves legacy skill parity while keeping outputs auditable.

## Mode Selection

- **Default**: `targeted` (run only relevant tracks, always produce final synthesis).
- **Full-Parallel**: run **all tracks** below, even if some are partially `SKIP` due to missing inputs.

Trigger Full-Parallel when user says: “全量”, “并行”, “run all tracks”, “run every skill”, “逐个 skill 测试”, “full pipeline”.

## Core Rule: Track Independence

Treat each track as an independent “mini-reviewer”:

- Do **not** reuse conclusions across tracks.
- Do **not** let one track’s framing bias another track’s critique.
- Do **not** remove findings because “another track already said it”.
- It is acceptable (and expected) to be redundant.

After all tracks finish, produce a synthesis that de-duplicates and resolves conflicts.

## Track List (Must Run in Full-Parallel)

Each track produces its own section in the final report. All tracks must be visible.

1) **Track A — Paper Self-Review (paper-level QA)**
   - Source: `references/modules/paper-self-review.md`
   - Output: structure/logic/citations/figures/writing checklist + findings

2) **Track B — Academic Paper Helper (LaTeX + templates + fix-ready text)**
   - Source: `references/modules/academic-paper-helper.md`
   - Output: concrete paste-ready text blocks and LaTeX troubleshooting notes

3) **Track C — ML Paper Writing (narrative + reviewer attacks)**
   - Source: `references/modules/claude-scholar-ml-paper-writing.md`
   - Output: What/Why/So-what + Top-5 likely reviewer attacks + defense text suggestions

4) **Track D — Anti-AI Polish**
   - Source: `references/modules/writing-anti-ai.md`
   - Output: pattern detection + rewrites + (optional) quick scoring rubric

5) **Track E — LaTeX Rhythm Refinement**
   - Source: `references/modules/latex-rhythm-refiner.md`
   - Output: 1–3 targeted rhythm rewrites + verification checklist (citations preserved)

6) **Track F — Citation Audit (Claim-level)**
   - Source: `references/modules/citation-validator.md` and `references/citation-integrity.md`
   - Output:
     - If bibliography/sources are missing: emit `SKIP` with a precise reason and what’s needed.
     - If sources exist: produce the legacy-style audit report.

7) **Track G — Rebuttal / Review Response**
   - Source: `references/modules/review-response.md` and `references/rebuttal-workflow.md`
   - Output:
     - If reviewer comments are provided: point-by-point rebuttal draft + revision plan.
     - If no comments: “rebuttal readiness pack” (Top-5 predicted comments + strategy + where to point in the paper).

## Post-Track Synthesis (Mandatory)

After all tracks:

1) Produce **Section-by-section review** (final, consolidated).
2) Produce **P0/P1/P2** prioritized issue list (final, de-duplicated).
3) Produce **Revision plan** (3–8 items) with acceptance criteria.
4) Produce **Conflicts & resolutions**:
   - List any disagreements between tracks.
   - Explain which recommendation is adopted and why.

