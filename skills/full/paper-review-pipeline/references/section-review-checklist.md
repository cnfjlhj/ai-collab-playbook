# Section Review Checklist (ICML / ICLR / NeurIPS / AAAI)

This is a *review checklist*, not a rigid template. Use it to detect gaps fast.

## Abstract

- Problem: is the task concrete and recognizable to the community?
- Method: is the core idea named and described (not “a novel framework”)?
- Results: are the *main numbers* stated with context (dataset/metric)?
- Contribution: are claims specific and falsifiable?
- Avoid: generic opening sentence that could fit any ML paper.

## Introduction

- Motivation: why should the ICML/ICLR/NeurIPS/AAAI reviewer care?
- Gap: what exactly is missing in prior work (1–2 sentences)?
- Contribution bullets: 2–4 bullets, each tied to evidence later (table/figure).
- Reader contract: what the paper will show, and how the sections map.
- Avoid: “We propose a novel method” without stating what is novel and why it matters.

## Related Work

- Positioning: what is the closest line of work, and how do you differ?
- Coverage: cite the *most relevant* works; do not turn into a bibliography dump.
- Narrative: group by theme; compare assumptions, not only outcomes.
- Avoid: listing papers with one sentence each and no synthesis.

## Method

- Problem setup: inputs/outputs/objective clearly defined; notation introduced once.
- Design rationale: why these components; what alternatives were rejected and why.
- Reproducibility: enough detail that an implementer can reproduce core method.
- Complexity/efficiency: mention compute/memory implications if relevant.
- Avoid: hiding key details in appendices when they are necessary to understand the method.

## Experiments / Results

- Setup completeness: datasets, splits, preprocessing, augmentation, metrics.
- Baselines: strongest and fairest; clarify if you used re-implementations.
- Training details: epochs, batch size, optimizer, LR schedule, early stopping.
- Reporting: multiple seeds; mean ± std/CI; significance tests when appropriate.
- Fairness: compare under similar compute budgets; report parameter counts when relevant.
- Avoid: only reporting the best run, or leaving the evaluation protocol implicit.

## Analysis / Ablations

- Claim-driven: each ablation ties to a specific design claim.
- Failure modes: where does it break; what patterns appear?
- Sensitivity: key hyperparameters; robustness to distribution shift if relevant.
- Avoid: “many plots” without a clear point that connects back to the paper’s thesis.

## Limitations / Broader Impact / Ethics (venue-dependent)

- Limitations: honest constraints; what settings are not covered.
- Risks: misuse, bias, privacy; not generic boilerplate.
- Avoid: exaggerated impact claims or vague “future work” filler.

## Figures / Tables (cross-cutting)

- Captions stand alone (a reviewer should understand without scanning the text).
- Axes/units labeled; legends readable; consistent notation across the paper.
- Tables include relevant context: dataset/metric/higher-is-better.
- Avoid: tiny text, unclear color palettes, missing error bars where variance matters.

## Citations (cross-cutting)

- Each major claim has either evidence (result/theorem) or a credible citation.
- Citation keys resolve; formatting consistent; no suspicious placeholders left.
- Avoid: citing papers you have not verified exist.

