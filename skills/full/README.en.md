# Public Full Skills

[中文](README.md) | English

Skills are workflows I've validated repeatedly and then formalized — not one-off prompts, but reusable processes with goals, steps, and acceptance criteria.

This is **not** a mirror of every private local skill I use. It is the subset I currently consider public-safe, useful, and worth sharing.

The skills are organized into four categories by scenario:

- **Research and Writing**: paper reading, review, anti-AI writing, video summaries, etc.
- **Planning, Collaboration, and Recovery**: proactive exploration, multi-perspective planning, requirement alignment, session recovery, skill governance, etc.
- **Multi-model Collaboration**: bridging and cross-validation between Claude, Codex, and Gemini
- **Publishing and Content Production**: Xiaohongshu notes, long-form publishing, etc.

Each skill directory contains at least a `SKILL.md` — that's the actual content. Start there.

If you want to go back to the repository homepage, see [`../../README.en.md`](../../README.en.md).

## Research and Writing

- [`academic-paper-helper/`](academic-paper-helper/): LaTeX, BibTeX, structure templates, and writing scaffolding for AI/ML papers.
- [`paper2html/`](paper2html/): convert paper PDFs, arXiv/OpenReview pages, or local LaTeX sources into Chinese HTML deep-reading pages with evidence boundaries, KaTeX formulas, figure/table maps, and pre-publication validation.
- [`paper-review-pipeline/`](paper-review-pipeline/): a local paper review workflow that combines section review, issue grading, citation checks, and rebuttal guidance.
- [`paperreview/`](paperreview/): a deterministic bridge to `paperreview.ai` for PDF submission and result polling.
- [`question-refiner/`](question-refiner/): refine a vague research topic into a structured deep-research brief before execution.
- [`writing-anti-ai/`](writing-anti-ai/): remove AI writing patterns without pretending to be a magic detector-evasion tool.
- [`timestamped-video-summary/`](timestamped-video-summary/): convert timestamped transcripts into strict, structured summaries and optionally export them to PDF.

## Planning, Collaboration, and Recovery

- [`proactive-explorer/`](proactive-explorer/): formalize the habit of exploring facts before asking the user for information.
- [`all-plan/`](all-plan/): a lightweight multi-perspective planning entry point with scoring and correction loops.
- [`human-machine-brainstorm/`](human-machine-brainstorm/): a CCB-flavored human-in-the-loop brainstorming workflow rather than a universal multi-agent framework.
- [`spec-first-mvp/`](spec-first-mvp/): add a small gate for exciting ideas by writing a spec seed, running a throwaway MVP probe, and only then deciding whether to enter full design or implementation.
- [`prompt-polisher/`](prompt-polisher/): turn messy notes or transcripts into a better prompt for Claude 4.x style workflows.
- [`session-recovery-codex/`](session-recovery-codex/): recover Codex session state from a session id or recent session list.
- [`skill-creator/`](skill-creator/): methods and tooling for turning personal workflows into reusable skills.
- [`skill-governance-loop/`](skill-governance-loop/): govern skills from real cases, version updates, and keep/disable/archive decisions while clarifying what belongs in `AGENTS.md` versus a skill.
- [`skills-governance/`](skills-governance/): filesystem-backed inventory and governance for large local skill collections.
- [`find-skills/`](find-skills/): search skills.sh first, then fall back to GitHub-based discovery.

## Multi-model Collaboration

- [`collaborating-with-claude/`](collaborating-with-claude/): bring Claude Code CLI into the workflow as a second opinion.
- [`collaborating-with-codex/`](collaborating-with-codex/): collaborate with a second Codex CLI session while keeping the current session responsible for verification.
- [`collaborating-with-gemini/`](collaborating-with-gemini/): bring Gemini CLI into the loop as a collaborator.

## Publishing and Content Production

- [`xhs-note-creator/`](xhs-note-creator/): Xiaohongshu note workflow from writing to card rendering and optional publishing.
- [`xhs-longform-private-publisher/`](xhs-longform-private-publisher/): publish an existing Markdown long-form post to Xiaohongshu in private mode with minimal rewriting.

## Notes

- This layer is best for readers who want to inspect the actual skill packages.
- Some skills may later be spun out into standalone repositories if they become mature enough for separate stars, forks, and public maintenance.
