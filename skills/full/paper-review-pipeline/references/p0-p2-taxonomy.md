# P0 / P1 / P2 Taxonomy (Paper Review)

Use this taxonomy to ensure review output is consistent and actionable.

## P0 — Blocking (likely rejection / not review-ready)

Typical P0s:
- **Claim-evidence mismatch**: core claims not supported by experiments/theory/citations.
- **Missing key baselines** for the stated problem (or unfair comparisons).
- **Experimental protocol unclear**: data splits, metrics, training details, compute not specified.
- **Statistical reporting missing** when variance matters (no seeds, no error bars, cherry-picked best run).
- **Citation integrity risk**: unverified citations, fabricated BibTeX, references do not support claims.
- **Paper cannot be followed**: definitions missing, method ambiguous, notation inconsistent.
- **Blind review violations** (if applicable): identity leaks, de-anonymization via links/self-cites.

Rule of thumb: if a reviewer can write “I cannot assess X because Y is missing/unclear”, it is probably P0.

## P1 — Important (moves acceptance probability)

Typical P1s:
- **Stronger framing**: sharper gap statement; contributions rewritten into verifiable claims.
- **Ablations** to validate key design choices.
- **Broader evaluation**: additional datasets, robustness tests, sensitivity analysis.
- **Better analysis**: error analysis, qualitative examples, failure modes.
- **Reproducibility upgrades**: hyperparameters, full training recipes, compute budget, code release plan.
- **Related work positioning**: clarify what is new vs prior art; cite the most relevant 5–10 works.
- **Writing clarity**: reduce cognitive load, improve transitions, define terms earlier.

Rule of thumb: if fixing it would improve reviewer confidence but the paper is still “evaluable” today, it is probably P1.

## P2 — Nice-to-have (polish)

Typical P2s:
- Typos, minor grammar, minor rewording.
- Small figure/table layout improvements.
- Extra citations that improve completeness but do not change claims.
- Optional appendix restructuring.

Rule of thumb: if reviewers would not mention it unless the rest is already strong, it is probably P2.

