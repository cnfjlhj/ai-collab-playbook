# AI Collab Playbook

[中文](README.md) | English

I'm a PhD student in AI. Since the GPT-3.5 days I've been using AI heavily across research, writing, coding, and everyday learning. This repo is the accumulation of that experience.

This is not a tool list or a prompt cookbook. The question I keep coming back to is: once AI can participate in all these activities, how do you keep owning the problem, judging the quality, building experience — and stop yourself from outsourcing understanding?

**Treat AI as a colleague, not a tool — but the human is still the main variable.** AI can explore, generate, and execute, but problem framing, acceptance criteria, trade-offs, and final judgment should stay with you. Otherwise higher efficiency just means producing the illusion of progress, faster.

## Start Here

- **Full article**: [`docs/phd-ai-collab.md`](docs/phd-ai-collab.md)
- **Quick overview**: the three figures below, then jump to the matching sections in the article.
- **Reusable workflows**: [`skills/full/README.en.md`](skills/full/README.en.md) and [`prompts/`](prompts)
- **How I constrain agents**: [`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md)

## What This Playbook Is About

**Human as the main variable.** AI amplifies capability, but it cannot replace problem awareness or judgment. You still need to know what you want, what counts as good, and what to drop.

**Colleague, not oracle.** Put AI into real workflows — not just Q&A windows. Selection-triggered tools, IM-based dispatch, remote agents: the closer the entry point is to your actual task, the more naturally AI gets used.

**Low-friction entry.** Not every task deserves a full agent pipeline. Lightweight one-off jobs should go to lightweight entry points — a selection toolbar, a chat message, a browser sidebar.

**Context first.** Prepare your goals, materials, preferences, and acceptance criteria before you hand off execution. AI output without context is barely better than dice rolls.

**Reusable practice.** Turn what works into Skills and Workflows — they get better and faster with reuse. But prune regularly; skill bloat is its own kind of noise.

**Anti-efficiency theater.** Beware of outsourcing understanding, taste, trade-offs, and learning itself to AI. Being efficient without understanding what you're doing is more dangerous than being slow.

[![PhD AI collaboration framework](docs/figs/phd-ai-agent-framework.png)](docs/phd-ai-collab.md#code-agent-framework)

## What's in This Repo

| Category | Entry | Description |
|----------|-------|-------------|
| Main article | [`docs/phd-ai-collab.md`](docs/phd-ai-collab.md) | Full methodology, 2026-06-08 edition |
| Agent rules | [`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md) | The rules I actually use to constrain AI agents |
| Prompts | [`prompts/`](prompts) | Reusable prompt templates: prompt polisher, concept explainer, paper reading, etc. |
| Full Skills | [`skills/full/README.en.md`](skills/full/README.en.md) | All in-repo public skills with descriptions |
| Figures | [`docs/figs/`](docs/figs) | Framework diagrams, learning guide, roadmap |

## Independent Skill Repos

These skills have been spun out into standalone repositories. They aren't meant to be installed all at once — pick what fits your workflow:

| Skill | Purpose |
|-------|---------|
| [paper-review-pipeline](https://github.com/cnfjlhj/paper-review-pipeline) | End-to-end paper review workflow |
| [paperreview](https://github.com/cnfjlhj/paperreview) | paperreview.ai bridge for second opinions |
| [skills-governance](https://github.com/cnfjlhj/skills-governance) | Skill inventory and governance |
| [session-recovery-codex](https://github.com/cnfjlhj/session-recovery-codex) | Codex session state recovery |
| [collaborating-with-codex](https://github.com/cnfjlhj/collaborating-with-codex) | Multi-Codex collaboration patterns |
| [completion-learn](https://github.com/cnfjlhj/completion-learn) | Three-axis retrospective after task completion: self, collaboration, tool |
| [xhs-note-creator](https://github.com/cnfjlhj/xhs-note-creator) | Xiaohongshu note creation pipeline |
| [prompt-polisher](https://github.com/cnfjlhj/prompt-polisher) | Turn rough notes into clean prompts |
| [writing-anti-ai](https://github.com/cnfjlhj/writing-anti-ai) | Remove AI-sounding patterns from writing |
| [xhs-longform-private-publisher](https://github.com/cnfjlhj/xhs-longform-private-publisher) | Publish Markdown long-form to Xiaohongshu |

## Feedback

- Comments and adaptations: [Discussions](https://github.com/cnfjlhj/ai-collab-playbook/discussions/1)
- Corrections or structural suggestions: [Open an issue](https://github.com/cnfjlhj/ai-collab-playbook/issues/new/choose)
- Xiaohongshu post: [link](https://www.xiaohongshu.com/discovery/item/69ab040f000000001a02d99e)

---

<details>
<summary>Star History</summary>

<a href="https://star-history.dera.page/#cnfjlhj/ai-collab-playbook&type=date&legend=top-left">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://star-history.dera.page/svg?repos=cnfjlhj%2Fai-collab-playbook&type=date&theme=dark&legend=top-left"
    />
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://star-history.dera.page/svg?repos=cnfjlhj%2Fai-collab-playbook&type=date&legend=top-left"
    />
    <img
      alt="Star History Chart"
      src="https://star-history.dera.page/svg?repos=cnfjlhj%2Fai-collab-playbook&type=date&legend=top-left"
    />
  </picture>
</a>

</details>
