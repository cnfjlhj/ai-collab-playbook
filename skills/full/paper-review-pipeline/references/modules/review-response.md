# Module: Review Response / Rebuttal (Feature-Parity Import)

This module preserves the distinctive workflow from the legacy `review-response` skill.

## Core Features to Preserve

1) Review analysis: parse and classify comments.
2) Response strategy: decide how to address each comment (accept/defend/clarify/add experiment).
3) Rebuttal writing: structured point-by-point document.
4) Tone management: professional, respectful, evidence-based.

## Workflow (Must Support)

Receive reviewer comments → parse & classify → strategy per comment → write responses → tone check → final rebuttal.

## Comment Classification (Must Support)

At minimum classify into:
- Major
- Minor
- Typo
- Misunderstanding / clarification-needed

Optionally track: missing baseline, missing experiment, writing clarity, citation request, ethics/broader impact.

## Strategy Library (Must Support)

For each comment select one:
- **Accept**: acknowledge + change paper.
- **Defend**: explain rationale with evidence; bound claims; concede limitations when real.
- **Clarify**: add intuition/definition; reorganize explanations.
- **Experiment**: add requested experiment/ablation or explain constraints with a substitute analysis.

## Output Requirements (Must Support)

- Ensure **every comment receives a response** (completeness).
- Keep responses skimmable and aligned with reviewer numbering.
- If changes are made, point to where: section/figure/table/appendix.
- Maintain respectful tone; avoid combative language.

## Tone Rules (Must Support)

- Thank reviewers for time and feedback.
- Assume misunderstandings are caused by unclear writing unless proven otherwise.
- Prefer factual language: “We clarify …”, “We updated …”, “Our results indicate …”.
- Avoid overpromising (“we will add extensive experiments”) unless feasible.

