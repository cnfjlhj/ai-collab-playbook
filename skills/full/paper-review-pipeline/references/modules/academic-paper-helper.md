# Module: Academic Paper Helper (LaTeX + BibTeX + Templates) — Feature-Parity Import

This module preserves the distinctive capabilities from the legacy `academic-paper-helper` skill: LaTeX scaffolding patterns, BibTeX hygiene, academic structure templates, and common LaTeX troubleshooting.

## 1) LaTeX Framework / Scaffolding (Must Support)

Provide a minimal working LaTeX skeleton with:
- Standard math + figure/table packages
- Venue style file placeholder (when applicable)
- Sections: Abstract, Introduction, Related Work, Method, Experiments, Conclusion, Bibliography

Key requirement: generate something concrete the user can fill, not only advice.

## 2) BibTeX Entry Hygiene (Must Support)

When user provides messy citation notes (title/authors/year/venue), the workflow must:
- Normalize author names
- Normalize title casing (avoid losing proper nouns)
- Add DOI/URL if available via verified sources (do not invent)
- Use stable citation keys if the user asks

Guardrail: do not fabricate BibTeX. If metadata is missing, ask for DOI/arXiv/URL or mark as placeholder.

## 3) Academic Writing Conventions Checklist (Must Support)

Language:
- Prefer formal academic tone (avoid colloquial phrases).
- Ensure paragraph coherence and consistent terminology.

Format:
- Figure/table numbering and referencing correct.
- Equation numbering and referencing correct.
- Citation format consistent.
- Acronyms defined on first use.

Content:
- Abstract length appropriate for venue norms.
- Introduction structure: motivation → problem → approach → contributions.
- Method: reproducible.
- Experiments: datasets/metrics/baselines/setup complete.

## 4) LaTeX Compilation Error Triage (Must Support)

Provide diagnosis patterns for common LaTeX errors:
- Undefined control sequence (missing package / typo)
- Missing `$` inserted (math mode mismatch)
- File not found (path issues for figures/bib)
- Citation undefined (bib compilation / wrong key)

## 5) Section Templates (Must Support)

### Introduction (template)
- Background/motivation
- Problem statement
- Approach overview
- Contribution bullets

### Method (template)
- Problem formulation
- Architecture
- Training / optimization
- Implementation details

### Experiments (template)
- Setup (datasets/baselines/metrics/implementation)
- Main results (table)
- Ablation study
- Analysis / qualitative results

## 6) Common LaTeX Snippets (Must Support)

- Algorithm environment skeleton
- Table skeleton with `booktabs`

Note: snippets should be given in a way that is safe to paste into LaTeX.

