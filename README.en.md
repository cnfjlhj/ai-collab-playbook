# AI Collab Playbook

[中文](README.md) | English

A Chinese-first personal playbook about **collaborating with AI in real work**: daily academic life, research reading, scientific writing, code-agent workflows, and periodic review.

This repository is not meant to present a universal “best practice”. It is a public-facing version of a workflow I have actually iterated on for years.

If you are new here, start with the main article: [`docs/phd-ai-collab.md`](docs/phd-ai-collab.md).

## Start Here

- **Main article (2026-03-06 edition)**: [`docs/phd-ai-collab.md`](docs/phd-ai-collab.md)
- **Linux.do discussion**: <https://linux.do/t/topic/1667121>
- **Xiaohongshu post**: <https://www.xiaohongshu.com/discovery/item/69ab040f000000001a02d99e?source=webshare&xhsshare=pc_web&xsec_token=LBModFyJ1bo4oqM2YmRbD3X0SpH1wO_Yo72JPNGieHJRo=&xsec_source=pc_share>
- **Agent rules**: [`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md)
- **Prompt collection**: [`prompts/`](prompts)
- **Skill catalog**: [`skills/README.en.md`](skills/README.en.md)
- **Public full skills**: [`skills/full/README.en.md`](skills/full/README.en.md)

## What You Will Find Here

- A long-form article on how a PhD student actually collaborates with AI in daily work.
- A pair of working rule files for agent collaboration, not just abstract advice.
- A set of prompts I reuse frequently in practice.
- A public collection of skills for paper review, session recovery, skill governance, prompt cleanup, and Xiaohongshu publishing workflows.

## Main Article

### [How I Collaborate with AI in Daily PhD Life](docs/phd-ai-collab.md)

The main article is the best entry point to this repository. It covers:

- AI as a daily advisor rather than a one-shot answer machine.
- A staged workflow for literature reading and knowledge integration.
- How I use AI for scientific figures without fully handing over judgment.
- Why writing with AI only works when the model actually understands the task.
- Why code-agent work needs exploration, alignment, execution, and verification.
- Why periodic review matters more than accumulating endless tools.

Related links:

- [`Read the full article`](docs/phd-ai-collab.md)
- [`View the figures`](docs/figs)

## Working Rules

If you want the most reusable part of this repo, start with:

- [`AGENTS.md`](AGENTS.md): execution rules for Codex and general agents
- [`CLAUDE.md`](CLAUDE.md): working rules for Claude Code style coding workflows

The core ideas are simple:

- Prefer executable delivery over abstract discussion.
- Reuse an existing skill before inventing a new workflow.
- Explore first, ask later.
- Align before execution.
- Back up before risky operations.
- Verify before claiming completion.

## Featured Skills

- [`paper-review-pipeline`](skills/full/paper-review-pipeline/): local paper review workflow with issue grading and revision guidance.
- [`paperreview`](skills/full/paperreview/): bridge to `paperreview.ai` for an external second opinion on near-final PDFs.
- [`skills-governance`](skills/full/skills-governance/): inventory and governance workflow for large local skill collections.
- [`session-recovery-codex`](skills/full/session-recovery-codex/): recover a Codex session and continue from the last real task state.
- [`collaborating-with-codex`](skills/full/collaborating-with-codex/): bring a second Codex CLI session into the workflow as a collaborator.
- [`prompt-polisher`](skills/full/prompt-polisher/): turn messy notes or transcripts into an executable prompt.
- [`writing-anti-ai`](skills/full/writing-anti-ai/): remove AI writing patterns while keeping the author's actual voice.
- [`xhs-longform-private-publisher`](skills/full/xhs-longform-private-publisher/): publish an existing Markdown long-form post to Xiaohongshu in private mode with minimal rewriting.

## Standalone Skill Repos

These are the current standalone skill repos that are easier to star, fork, and maintain on their own, while the mother repo keeps the long-form article and overall context.

- [`paper-review-pipeline`](https://github.com/cnfjlhj/paper-review-pipeline): the standalone local paper-review workflow.
- [`paperreview`](https://github.com/cnfjlhj/paperreview): the standalone external second-opinion bridge to `paperreview.ai`.
- [`skills-governance`](https://github.com/cnfjlhj/skills-governance): the standalone inventory and governance tool for local skill collections.
- [`session-recovery-codex`](https://github.com/cnfjlhj/session-recovery-codex): the standalone task-context recovery toolkit for local Codex sessions.
- [`collaborating-with-codex`](https://github.com/cnfjlhj/collaborating-with-codex): the standalone bridge for collaborating with a second Codex CLI session.
- [`xhs-note-creator`](https://github.com/cnfjlhj/xhs-note-creator): the standalone Xiaohongshu note-production toolkit for themed cards and optional publishing.

For the full in-repo directory view, see [`skills/README.en.md`](skills/README.en.md) and [`skills/full/README.en.md`](skills/full/README.en.md).

## Notes

- This is a **Chinese-first** repository. Most prompts, the main article, and many skill notes are written in Chinese.
- The public files here are the versions I consider safe and worth sharing, not a mirror of every private local setup.
- The current standalone skill repositories are linked above. If more skills mature into stronger independent projects, I will spin them out while keeping this repo as the mother repo / overview layer.
