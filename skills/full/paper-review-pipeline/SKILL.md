---
name: paper-review-pipeline
description: Use when a mostly complete ML conference paper needs self-review, pre-submission QA, camera-ready checking, section-by-section critique, citation-risk inspection, or rebuttal/review-response drafting. Skip this for initial drafting and use `paperreview` only when the user explicitly wants external submission.
---

# Paper Review Pipeline (ML Top Conferences)

Run a *two-view* paper review for ML conference submissions:

1) **Section-by-section review** (Abstract → Intro → Method → Experiments → …) with concrete edits.
2) **Prioritized issue list** with **P0/P1/P2** severity, grouped by category, including recommended fixes and verification notes.

This skill also supports **rebuttal / review response**: parse reviewer comments, classify, choose a strategy, and draft a professional point-by-point response.

## Parity Guarantee (No-Omission)

This skill is a consolidation layer. It must **not** omit any distinctive workflow, constraints, or output formats from the legacy skills it replaces.

Use:
- `references/parity-matrix.md` as the feature-parity contract and regression scenarios.
- `references/modules/` for full imported workflows and checklists.

## Execution Modes

This skill supports two modes:

- **Default: `targeted`** — run only the most relevant tracks based on the user request and inputs, but **always** produce the Final Synthesis.
- **Optional: `full-parallel`** — run **all tracks** as independent outputs (acceptable redundancy), then produce the Final Synthesis.

Trigger `full-parallel` when the user says: “全量”, “并行”, “run all tracks”, “run every skill”, “逐个 skill 测试”, “full pipeline”.

Protocol + required report template:
- `references/full-parallel-protocol.md`
- `references/report-template.md`

## Optional External Second Opinion (`paperreview`)

If the user provides a near-final or final PDF, complete the local review first and then explicitly ask whether they also want an external second opinion via `paperreview`.

- Ask only when the input is clearly a near-final or final PDF.
- Do **not** auto-submit to external services. Get explicit confirmation first.
- If the user agrees, hand off to `paperreview` as a follow-up step; otherwise finish with the local pipeline result only.

## When to Use

- Pre-submission quality check (ICML/ICLR/NeurIPS/AAAI).
- After a draft is “mostly done” but clarity/logic is shaky.
- When you suspect citation problems (missing, inconsistent, unverified, or claim-to-citation mismatch).
- Before sending to advisor/collaborators for feedback (to reduce “obvious issues”).
- After receiving reviews: draft rebuttal and a revision plan.

## When NOT to Use

- If the user wants **new research** or **new experiments** invented: require the user to provide results/artifacts.
- If the user asks for **verbatim PDF-to-LaTeX copying** or large-scale reformatting without source.
- If the task is **pure BibTeX generation from memory**: do not do it; use verified metadata workflows.

## Non-Negotiable Guardrails

1) **No hallucinated citations.**
   - If a citation cannot be verified, mark it as `[CITATION NEEDED]` / placeholder and tell the user explicitly.
   - Do not fabricate authors/years/venues/DOIs.
2) **Do not change technical meaning.**
   - When proposing edits, preserve claims and numbers unless the user provides corrected data.
3) **Preserve LaTeX semantics when editing source.**
   - Do not break `\\cite{}`, `\\ref{}`, `\\label{}`, math environments, figures/tables, or bibliography hooks.
4) **Respect blind review constraints (if applicable).**
   - Avoid identity-revealing self-citations, acknowledgments, or repo links unless the user confirms it is camera-ready.

## Inputs (Ask for the Minimum Needed)

### For pre-submission review
- Paper source: LaTeX section text, or the relevant excerpts pasted in chat (preferred), and optionally the PDF for context.
- Target venue + track (ICML/ICLR/NeurIPS/AAAI) and any required sections (e.g., limitations / broader impact / ethics).
- One-sentence contribution (if the user has it). If not, infer and ask for confirmation.

### For rebuttal / review response
- Reviewer comments (verbatim text, ideally grouped by reviewer).
- Rebuttal constraints: word/page limit, formatting (ICLR OpenReview vs PDF), and timeline.
- What the user is willing to change: “clarify only” vs “add experiments” vs “major rewrite”.

## Output Contract (Always Produce Both Views)

### View A — Section-by-Section Review

For each section, output:
- **What works** (1–3 bullets)
- **What’s missing / unclear** (P0/P1/P2 tagged bullets)
- **Concrete fixes** (rewrite suggestions or structural moves)

Use the checklists in:
- `references/section-review-checklist.md`

### View B — P0/P1/P2 Issue List (Prioritized)

Format each issue like:
- **Priority**: P0 (blocking) / P1 (important) / P2 (nice-to-have)
- **Category**: Narrative / Evidence / Experimental Design / Statistics / Reproducibility / Citations / Writing / Figures-Tables / Format
- **Where**: section name + a short quote anchor (or LaTeX label if available)
- **Problem**
- **Fix**
- **Verification** (if needed): what evidence/log/search is required before claiming it is correct

Use the taxonomy in:
- `references/p0-p2-taxonomy.md`

## Modules (Routing Rules)

Use these modules to preserve legacy feature parity:

- **Paper-level QA**: `references/modules/paper-self-review.md`
- **Rebuttal / review response**: `references/modules/review-response.md` and `references/rebuttal-workflow.md`
- **LaTeX + BibTeX toolbox**: `references/modules/academic-paper-helper.md`
- **Claim-level citation audit**: `references/modules/citation-validator.md` and `references/citation-integrity.md`
- **Anti-AI polish**: `references/modules/writing-anti-ai.md`
- **LaTeX rhythm pass**: `references/modules/latex-rhythm-refiner.md`
- **Literature discovery (extended)**: `references/modules/claude-scholar-ml-paper-writing.md`

## Workflow (Default)

### Pass 0 — Triage (5–10 minutes)

1) Identify the **one-sentence contribution** and confirm it with the user.
2) Extract the **top 3–7 claims** the paper relies on.
3) For each claim, note the current support:
   - empirical result (table/figure)
   - theorem/proof
   - citation / prior work
   - ablation / analysis
4) Flag immediate P0 risks (typical: missing baselines, unclear experimental protocol, unverified citations, paper “about X” but experiments test Y).

### Pass 1 — Section Review (primary deliverable)

Review sections in order (and check alignment between them):
1) Abstract
2) Introduction (motivation → gap → contribution bullets)
3) Related Work (positioning + not a bibliography dump)
4) Method (reproducible description + design justification)
5) Experiments / Results (fair baselines + full setup + statistical reporting)
6) Analysis / Ablations (claim-driven, not exploratory noise)
7) Limitations / Broader Impact / Ethics (venue-dependent)
8) Conclusion (tight restatement + constraints + future work without overclaim)

### Pass 2 — Consolidate into P0/P1/P2

Turn findings into an actionable issue list:
- P0 first (blockers / likely desk-reject causes)
- P1 next (acceptance probability movers)
- P2 last (polish)

### Pass 3 (Optional) — Revision Plan

If the user wants an execution plan, produce:
- 3–8 tasks with measurable acceptance criteria
- suggested order (dependency-aware)
- what can be done in parallel (writing vs experiments vs citations)

## Full-Parallel Workflow (Comprehensive)

When mode is `full-parallel`, do not collapse everything into one voice. Instead:

1) Run all tracks (A–G) as independent “mini-reviewers” and keep each track output visible.
2) Then produce the Final Synthesis:
   - View A: consolidated section-by-section review
   - View B: consolidated P0/P1/P2 issue list
   - minimal revision plan
   - conflicts & resolutions between tracks

Use:
- `references/full-parallel-protocol.md`
- `references/report-template.md`

## Rebuttal / Review Response Module

When reviews arrive, do:
1) Parse and classify each comment: **Major / Minor / Clarification / Missing baseline / Missing experiment / Writing / Citation / Misunderstanding**.
2) Choose a strategy per item: **Accept + change**, **Clarify**, **Defend**, **Add experiment**, **Defer (explain constraints)**.
3) Draft point-by-point responses with:
   - gratitude + precise restatement
   - what changed (or why not)
   - where to find it (section/figure/table)
   - evidence-based tone (no overpromising)

Use:
- `references/rebuttal-workflow.md`

## Citation Integrity Module (Hard Requirement)

Before submission, ensure:
- every non-trivial factual claim has a citation or empirical evidence
- every citation key resolves in the bibliography
- any newly added citations are verified (paper exists; BibTeX not fabricated)

If deep citation audit is requested, follow:
- `references/citation-integrity.md`
