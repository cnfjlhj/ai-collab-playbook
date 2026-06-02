---
name: paper2html
description: Use when turning an academic paper PDF/arXiv/OpenReview page/local LaTeX source into a single-file Chinese HTML deep-reading page, especially when the user wants a Cheat-Sheet style explanation, KaTeX formulas, figure/table evidence, validation, or a publishable research page.
---

# Paper2HTML

## Overview

Create one self-contained Chinese `index.html` that lets the user read the page and understand the paper without reopening the PDF. Default style: clear Cheat-Sheet page, focused evidence, KaTeX formulas, no decorative complexity.

Use scripts first. Keep this skill as workflow/quality gates, not a long prompt.

## Scripted Path

```bash
cd /path/to/paper2html

# 1) Create workspace + source-boundary note + starter index.html
python scripts/bootstrap_paper2html.py \
  --title "Paper Title" \
  --slug paper-slug \
  --out /path/to/output/paper-slug-html-YYYYMMDD \
  --arxiv 2504.07952 \
  --github https://github.com/org/repo \
  --publish-to self-evolving-agent/topic/paper-slug

# 2) If TeX/source exists, create a structural inventory
python scripts/tex_inventory.py \
  /path/to/output/source/unpacked \
  --out /path/to/output/notes/tex-inventory.md \
  --json /path/to/output/notes/tex-inventory.json

# 3) Optimize figures and get data URIs for single-file HTML
python scripts/optimize_paper_images.py \
  paper_figures/*.pdf paper_figures/*.png \
  --out-dir /path/to/output/assets/optimized \
  --width 1600 \
  --data-uri-json /path/to/output/assets/data-uris.json

# 4) Optional but preferred: ask Gemini for a visual draft on a copy
scripts/gemini_frontend_pass.sh \
  /path/to/output/index.html \
  --reference /path/to/good-reference.html \
  --timeout 240

# To inspect the exact Gemini prompt and attached materials without spending a model call:
scripts/gemini_frontend_pass.sh \
  /path/to/output/index.html --dry-run

# 5) Validate final HTML after Codex merges the useful visual changes and
#    fills/repairs the paper details.
scripts/validate_paper_html.sh \
  /path/to/output/index.html --public

# 6) Optional: publish through a compatible research-page importer.
#    Requires PAPER2HTML_BLOG_ROOT and a repo that provides `pnpm research:publish`.
PAPER2HTML_BLOG_ROOT=/path/to/blog \
PAPER2HTML_PUBLIC_BASE_URL=https://example.com/research \
scripts/publish_paper2html.sh \
  /path/to/output/index.html \
  --to self-evolving-agent/topic/paper-slug \
  --title "Paper Title" \
  --description "One sentence summary" \
  --tags "paper-reading,agent" \
  --ship
```

## Workflow

1. **Freeze source boundary**
   - Treat user input as a locator for one paper, then look for public adjacent artifacts: arXiv source/PDF, OpenReview, proceedings, project page, GitHub, appendix, dataset/model cards.
   - Run `bootstrap_paper2html.py` when starting from a known title/arXiv/GitHub. Otherwise manually create the same `notes/source-boundary.md`.
   - Separate **reading sources** from **public evidence sources**. Public pages must not expose local paths, private source filenames, review metadata, private prompts, or run logs.
   - If public publishing is requested and no public paper source exists, generate private HTML only and do not publish.

2. **Extract material**
   - Prefer TeX/source packages over PDF-only reading. Run `tex_inventory.py` when source exists.
   - Build a paper material pack: metadata, outline, claims, notation, equations, algorithms, figure/table map, experiment map, appendix details, public links.
   - Use PDF rendering for visual verification and figure/table placement. `pdftotext` is only an auxiliary index.
   - Before inserting any figure/table, record: original caption, page/source, what the visual/table itself shows, allowed HTML caption, and any nearby callout needed for broader interpretation.
   - Extract reproducibility details: datasets, splits, models, baselines, metrics, prompts, tool/prover/solver versions, decoding, timeouts, retries, appendix-only settings.

3. **Write the page**
   - Use a two-stage authoring path when visual quality matters:
     1. Codex builds the source-faithful content skeleton from the material pack.
     2. Gemini produces a visual draft on `index.gemini-draft.html` with
        `gemini_frontend_pass.sh`, using
        `prompts/gemini-initial-html.md` as the initial prompt. The script
        auto-attaches common notes from `<output>/notes/`: `material-pack.md`,
        `tex-inventory.md`, `figure-table-map.md`, and `source-boundary.md`.
     3. Codex manually merges the useful layout/style changes back into
        `index.html`, then adds missing paper details, formulas, figures,
        tables, evidence boundaries, and reviewer comments.
   - Gemini may improve visual hierarchy, spacing, typography, callouts,
     responsive behavior, and component composition. It must not become the
     source of factual paper content.
   - Use the fixed section order unless the paper demands a small adjustment:
     `先给结论`, `研究动机`, `数学表示及建模`, `算法流程/方法`, `实验设计`, `实验结果`, `我的评论`, `One More Thing`, `Reference / Evidence`.
   - Add a short version note near the top: reading basis and retrieval date, without local paths.
   - Write as deep-reading Cheat-Sheet, not abstract translation. The page should recover motivation, modeling, method, experiments, results, and reviewer-level caveats.
   - Bind each major claim to evidence and state boundaries when evidence does not support a stronger conclusion.
   - Use Chinese by default; keep paper terms, model names, datasets, commands, and identifiers in English.
   - Use KaTeX for all math. Inline math uses `\(...\)` or `$...$`; block math uses `$$...$$` or `\[...\]`.
   - Figure/table captions are evidence-local: captions may only claim what the displayed visual/table itself shows. Broader interpretation goes in a nearby callout.
   - `One More Thing` is for bounded research insight, not unsupported extrapolation.

4. **Reference policy**
   - Public page: `Reference / Evidence` contains only public online links.
   - Do not include `/home/...`, `main.tex`, `sections/...`, `appendices/...`, private PDF paths, hidden prompts, unpublished logs, or private run roots.
   - If no public source exists, say the page is private-only and do not publish.

5. **Validate**
   - Run `scripts/validate_paper_html.sh <index.html>` from this skill.
   - It checks: file exists, no placeholders, no local-path leaks in public mode, KaTeX initializes, no `katex-error`, desktop screenshot, mobile screenshot, no mobile horizontal overflow.
   - If `index.gemini-draft.html` was created, compare it against `index.html`
     and merge only design improvements that preserve source-faithful content.
   - For user-visible artifacts, deliver through the active collaboration channel when the host environment supports file delivery; otherwise provide the local path and validation result.

6. **Publish**
   - For repositories with a compatible `pnpm research:publish` command, use the optional one-step publisher:
     `PAPER2HTML_BLOG_ROOT=/path/to/blog scripts/publish_paper2html.sh <index.html> --to=<topic/series/slug> --title="..." --description="..." --tags="..." --ship`
   - Use `--check` for import plus local validation without commit/push.
   - `--ship` runs: paper HTML validation, public evidence guard, import, Prettier formatting of touched research files, `format:check`, lint, build, commit, push, deploy-workflow watch, and remote URL verification.
   - The publisher calls the target repo's `pnpm research:publish` control script, so the target repo owns staging, commit, and deploy behavior.
   - If a remote deploy check is not needed, pass `--no-watch` or `--no-remote-verify`.
   - Do not commit or push unless the user explicitly asks for git history updates.

## Template

- `assets/cheatsheet-template.html` is the fixed visual skeleton. Copy it into the output directory when starting a new page, then fill content and embed images.
- Keep the template simple. Do not turn paper pages into a marketing landing page.
