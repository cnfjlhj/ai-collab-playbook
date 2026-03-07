# Paper Review Pipeline — Feature Parity Matrix

This file is the “no-regression contract” for consolidating multiple paper-writing/review skills into `paper-review-pipeline`.

It serves two purposes:
1) **Parity matrix**: prove every legacy skill’s distinctive workflow/guardrails/output is present.
2) **Regression scenarios**: pressure tests to verify the pipeline output still includes all required elements.

If any row is not satisfied, treat it as **P0** and update `paper-review-pipeline` modules before disabling more legacy skills or relying on the pipeline for submission-critical work.

## Parity Matrix (Legacy → Pipeline)

### 1) `paper-self-review` (paper-level QA)

- **Legacy distinctive features**
  - Systematic self-review across: structure → logic → citations → figures/tables → writing clarity.
  - A compact “paper quality checklist”.
  - Explicit “when to use” stages: after first draft, pre-submission, post-revision verification.
- **Pipeline module**
  - `references/modules/paper-self-review.md`
- **Pipeline integration points**
  - Section-by-section pass uses the legacy structure categories.
  - P0/P1/P2 list must include “Structure completeness” and “Logic consistency” categories.

### 2) `review-response` (rebuttal workflow)

- **Legacy distinctive features**
  - Parse & classify reviewer comments, then select response strategy per comment.
  - Generate structured rebuttal; tone management; completeness across all comments.
  - “Accept/Defend/Clarify/Experiment” decision set.
- **Pipeline module**
  - `references/modules/review-response.md`
- **Pipeline integration points**
  - Rebuttal mode must output: classification + strategy + point-by-point draft + tone constraints + revision plan.

### 3) `academic-paper-helper` (LaTeX + BibTeX + structure snippets)

- **Legacy distinctive features**
  - Conference LaTeX skeleton generation patterns (NeurIPS/ICML/ICLR/AAAI/etc.).
  - BibTeX cleanup rules + example.
  - Common LaTeX compile errors diagnosis.
  - Section templates for Intro/Method/Experiments and common LaTeX snippets (algorithms, tables).
- **Pipeline module**
  - `references/modules/academic-paper-helper.md`
- **Pipeline integration points**
  - When user asks for “template / structure / LaTeX snippet / compile error”, route to this module.

### 4) `citation-validator` (claim-level citation audit)

- **Legacy distinctive features**
  - Claim detection → citation presence → completeness → source quality A–E → accuracy verification.
  - Output: structured “Citation Validation Report” with metrics and prioritized fixes.
  - Chain-of-verification for high-stakes claims.
- **Pipeline module**
  - `references/modules/citation-validator.md`
- **Pipeline integration points**
  - In “citation audit mode”, output must follow the legacy report structure (executive summary + critical issues + detailed findings + recommendations).

### 5) `writing-anti-ai` (anti-AI writing patterns removal)

- **Legacy distinctive features**
  - Pattern taxonomy (filler phrases, formulaic structures, rhythm, undue emphasis, vague attributions, AI vocabulary).
  - A concrete “quick scoring” rubric.
  - Bilingual (Chinese/English) handling.
- **Pipeline module**
  - `references/modules/writing-anti-ai.md`
- **Pipeline integration points**
  - In “polish/humanize” requests, apply the quick rules, then (optionally) apply the scoring rubric.

### 6) `latex-rhythm-refiner` (LaTeX prose rhythm pass)

- **Legacy distinctive features**
  - Strict constraints: do not add/remove/relocate citations; do not alter LaTeX structure/commands.
  - Workflow + verification checklist.
- **Pipeline module**
  - `references/modules/latex-rhythm-refiner.md`
- **Pipeline integration points**
  - In “final polish / rhythm pass” requests, enforce constraints and output verification checklist results.

### 7) `claude-scholar-ml-paper-writing` (extended ML writing workflow)

- **Legacy distinctive features**
  - A strong “never hallucinate citations” rule and proactive drafting posture.
  - Literature research & paper discovery workflow with screening + quality scoring.
  - Paper discovery process + “evaluate paper quality” rubric + knowledge growth idea.
- **Pipeline module**
  - `references/modules/claude-scholar-ml-paper-writing.md`
- **Pipeline integration points**
  - Keep the “proactive drafting” stance and “never hallucinate citations” rule consistent with pipeline guardrails.
  - When user asks “find related work / discover papers / literature review”, route to the discovery workflow.

## Regression Scenarios (Manual Acceptance Tests)

These are “pressure tests”. For each scenario, check that pipeline output includes the **Required elements** verbatim as categories/fields (not necessarily identical wording), and that constraints are respected.

### R1 — Full paper self-review (structure + logic + citations + figs + writing)

- **Input**: user provides Abstract + Intro + Method + Experiments excerpts; asks “pre-submission check”.
- **Required elements**
  - Section-by-section review covering at least Abstract/Intro/Method/Experiments.
  - A P0/P1/P2 list that includes: Structure, Logic consistency, Citations, Figures/Tables, Writing clarity.
  - At least one concrete rewrite suggestion (not only critique).
- **Must not happen**
  - Generic advice only; missing any of the five categories above.

### R2 — Rebuttal: classify → strategy → point-by-point

- **Input**: reviewer comments (10–30 bullets).
- **Required elements**
  - Each comment is classified (Major/Minor/…).
  - Each comment has a strategy (Accept+Change / Clarify / Defend / Add experiment / Defer).
  - Draft rebuttal text: point-by-point, skimmable.
  - A minimal revision plan (3–8 items).
- **Must not happen**
  - Skipping comments; combative tone; promising experiments without stating feasibility.

### R3 — Citation audit report (claim-level)

- **Input**: a list of 8–15 factual claims (or a paragraph with claims) + existing citations.
- **Required elements**
  - Claim detection (explicit list or enumerated claims).
  - Citation completeness checks (author/date/title/url/doi/pages when applicable).
  - Source quality grading A–E (if the user wants grading).
  - A structured report with summary metrics + critical issues + recommendations.
- **Must not happen**
  - Fabricated citations; confident verification claims without a source.

### R4 — Anti-AI pass

- **Input**: user says “this paragraph sounds AI-ish, humanize it”.
- **Required elements**
  - Identify at least 3 pattern types (e.g., filler, formulaic structure, vague attribution).
  - Produce a revised version + brief rationale.
  - Optionally provide the quick scoring rubric (1–10 per dimension) if asked.
- **Must not happen**
  - Inflated promotional tone; replacing technical terms without permission.

### R5 — LaTeX rhythm refinement with citation-preservation constraints

- **Input**: LaTeX section text containing `\\cite{...}` and references to figures/tables.
- **Required elements**
  - Revised LaTeX that preserves all `\\cite{...}` exactly (count and keys).
  - Explicit verification checklist: citation count unchanged; no LaTeX structure breakage.
- **Must not happen**
  - Moving a citation to a different claim; rewriting LaTeX environments incorrectly.

### R6 — Literature discovery for Related Work

- **Input**: user asks “help me find related work and position my paper”.
- **Required elements**
  - A systematic search/screen/evaluate/select workflow.
  - Quality scoring rubric and selection criteria.
  - Strong citation integrity warning: placeholders allowed; no fabricated BibTeX.
- **Must not happen**
  - Hallucinated references; dumping a long unstructured list of papers.

### R7 — Full-Parallel report completeness (track visibility + synthesis)

- **Input**: user explicitly requests “全量并行 / run all tracks / 逐个 skill 测试 / full pipeline”.
- **Required elements**
  - Report includes all track sections A–G (even if some are `SKIP` due to missing inputs).
  - Each track output is visible as its own section (not merged away).
  - Final Synthesis exists and includes:
    - consolidated section-by-section review
    - consolidated P0/P1/P2 list
    - minimal revision plan
    - conflicts & resolutions
- **Must not happen**
  - Only a synthesis without per-track outputs.
  - Hiding or deleting redundant findings instead of de-duplicating in synthesis.
