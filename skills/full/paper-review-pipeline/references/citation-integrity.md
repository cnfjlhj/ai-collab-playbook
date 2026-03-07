# Citation Integrity (No-Hallucination)

This module is for any request that involves adding, validating, or auditing citations.

## Non-Negotiable Rules

- Do not fabricate citations, DOIs, authors, venues, or BibTeX.
- If a citation cannot be verified, mark it as `[CITATION NEEDED]` / placeholder and tell the user.

## Minimal Checks (always)

- Every `\\cite{key}` resolves to an entry in the `.bib` file.
- Every non-trivial factual claim is backed by either:
  - an empirical result in the paper (table/figure), or
  - a verified citation.
- Newly added citations are verified to exist and to support the attributed claim.

## Deep Audit (when requested)

Produce a report with:
- Total claims checked
- Claims missing citations
- Citations missing metadata (author/year/title/url/doi)
- Citations that do not support the attributed claim
- Source quality notes (A–E, if the user wants this grading)

## Recommended Tooling (optional, if available)

If the workspace already uses paper notes + auditable verification records:
- Use a “BibTeX + verification record” workflow (e.g., `ref.bib` + `verified.jsonl`) so citations remain traceable.

If the user wants database/search-based citation lookup:
- Prefer scholarly metadata sources (CrossRef, arXiv, Semantic Scholar) over memory.

