# Rebuttal Workflow (Point-by-Point)

Goal: maximize reviewer confidence with minimal text. Be concrete, evidence-based, and easy to skim.

## Inputs to Request (minimal)

- Reviewer comments (verbatim), grouped by reviewer if possible.
- Rebuttal limit (word/page), format, and deadline.
- What can change: clarify-only vs add experiments vs major rewrite.

## Step 1 — Parse & Classify

For each comment, assign:
- **Type**: Major / Minor / Clarification / Missing baseline / Missing experiment / Writing / Citation / Misunderstanding / Ethics
- **Decision**: Accept+Change / Clarify / Defend / Add experiment / Defer (with constraints)

## Step 2 — Response Strategy (per comment)

### Accept + Change
- Acknowledge.
- State exactly what changed.
- Point to location: section/figure/table/appendix.

### Clarify
- Restate the reviewer’s confusion precisely.
- Provide the missing intuition/definition.
- If you changed text, say where; if not, give the crisp explanation anyway.

### Defend
- Do not argue tone-first. Argue evidence-first.
- Provide a short rationale + supporting result or citation.
- If a limitation exists, concede it cleanly and bound the claim.

### Add Experiment
- Specify what will be added (dataset, baseline, metric, ablation).
- If already done, report the result with context.
- If not feasible in time, defer with a principled reason and a plan.

### Defer (constraints)
- Keep it brief, factual, non-defensive.
- Offer a smaller substitute analysis when possible.

## Step 3 — Draft Template (per reviewer)

Use this structure:

1) 1–2 sentences of thanks + summary of the main improvements.
2) Numbered list of responses matching the reviewer’s numbering.

For each item:
- **Reviewer concern (quoted or paraphrased in one line)**
- **Response** (2–6 lines)
- **Change** (optional): “We updated Section X / Figure Y …”

## Tone Rules

- Be polite but not verbose.
- Never say “the reviewer is wrong”.
- Prefer “We agree and updated …” / “We clarify that …” / “Our results indicate …”.
- Avoid promising experiments you will not deliver.

## Output to Produce

Always provide:
- A point-by-point draft rebuttal text
- A minimal revision plan (3–8 items) mapping to the rebuttal

