# Module: Citation Validator (Claim-Level Audit) — Feature-Parity Import

This module preserves the “citation audit” workflow and report format from the legacy `citation-validator` skill.

## Core Responsibilities (Must Support)

1) Verify citation presence for every factual claim.
2) Validate citation completeness (required metadata).
3) Assess source quality (A–E).
4) Check citation accuracy (source supports claim).
5) Detect hallucinations (unsupported claims / non-existent sources).
6) Enforce consistent formatting.

## Citation Completeness Requirements (Must Support)

Each citation should include (as applicable):
- Author/Organization
- Publication date (at least year)
- Source title
- URL/DOI (verifiable)
- Page numbers (for PDFs/long docs when relevant)

## Source Quality Rating (Must Support)

- A: peer-reviewed meta-analyses, strong journals, government regulators
- B: solid studies/guidelines, reputable analysts, government sites
- C: case reports, company whitepapers, reputable news
- D: preprints, blogs without oversight
- E: anonymous/broken links/clear bias

## Validation Process (Must Support)

1) Claim detection: enumerate factual claims.
2) Citation presence: each claim has a citation.
3) Completeness: check required elements.
4) Quality rating: A–E per source.
5) Accuracy verification: confirm the source actually supports the claim.
6) Hallucination detection: flag missing/invalid/mismatched citations.
7) Chain-of-verification for critical claims (2–3 independent sources).

## Output Format (Must Support)

Produce a report with:

- Executive summary metrics (counts/percentages)
- Critical issues (immediate action required)
- Detailed findings (claim-by-claim)
- Recommendations (prioritized)

If the user requests it, include an overall quality score (0–10) and average source quality.

## Safety Rules (Hard)

- Never fabricate citations.
- If verification cannot be completed, label items as “needs manual verification” and explain what to check.

