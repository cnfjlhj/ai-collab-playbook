# AI Collab Playbook

[中文] | [English](README.en.md)

这是一个由一名在读博士生维护、以 **AI 协作实践** 为核心的个人 playbook，主要收录长期使用的 prompts、skills，以及围绕“博士生日常如何与 AI 协作”的持续更新内容。

这更像是一份长期打磨的个人工作流记录，而不是什么“通用最优解”。如果你也在把 AI 当同事协作，而不是只把它当工具，里面的大部分东西应该都能直接给你一些启发。

如果你是第一次来到这个仓库，我最建议你先看 [`docs/phd-ai-collab.md`](docs/phd-ai-collab.md)。

## 快速开始

- **最新文章（2026-03-06 版）**：[`docs/phd-ai-collab.md`](docs/phd-ai-collab.md)
- **Linux.do 讨论帖**：<https://linux.do/t/topic/1667121>
- **小红书发布版（当前分享链接）**：<https://www.xiaohongshu.com/discovery/item/69ab040f000000001a02d99e?source=webshare&xhsshare=pc_web&xsec_token=LBModFyJ1bo4oqM2YmRbD3X0SpH1wO_Yo72JPNGieHJRo=&xsec_source=pc_share>
- **AI 协作守则**：[`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md)
- **Prompts**：[`prompts/`](prompts)
- **Skills 总览**：[`skills/README.md`](skills/README.md)
- **完整公开版 Skills**：[`skills/full/README.md`](skills/full/README.md)

## 你可以从这里拿走什么

- 一篇围绕“博士生日常如何与 AI 协作”的完整长文，而不是只有零散技巧。
- 一套长期实际使用后沉淀下来的 agent 协作守则：什么时候先探索，什么时候该停下来对齐，什么时候必须先验证再说完成。
- 一批我日常会反复用到的 prompts，适合直接拿去改成自己的版本。
- 一组已经公开的 skill，包括论文自审、会话恢复、技能治理、prompt 整理、小红书发布等具体工作流。
- 一条更适合 GitHub 浏览的入口路径：先看文章，再看守则，再按需进入 prompts 和 skills。

## 主文章

### [作为一名在读博士生，我在日常是如何与 AI 协作的？](docs/phd-ai-collab.md)

这篇文章是目前仓库里最适合直接阅读的主内容。我把自己这些年在 **日常使用、科研阅读、科研绘图、科研写作、Code Agent 使用、复盘** 里的真实经验系统整理了一次，尽量保留实践细节。

你会在这篇文章里看到：

- 日常场景里如何把 AI 当作随身顾问，而不是一次性问答机。
- 科研文献阅读里，如何把课题调研、文献网络分析、精读和知识整合拆成不同阶段。
- 科研绘图里，怎样让 AI 帮忙，但不把判断权完全交出去。
- 科研写作里，为什么“让 AI 多审几遍”和“它真的理解对了”是两回事。
- Code Agent 工作流里，为什么我要反复强调先探索、再对齐、再执行、再验证。
- 为什么我会定期复盘，并把 prompt 和 skill 沉淀成更稳定的协作资产。

建议搭配一起看：

- [`阅读全文`](docs/phd-ai-collab.md)
- [`查看配图`](docs/figs)

## 协作守则摘录

如果你只想先抓住这个仓库里最有辨识度的一部分，我会优先推荐这两份文件：

- [`AGENTS.md`](AGENTS.md)：偏向 Codex / 通用 agent 协作的执行原则
- [`CLAUDE.md`](CLAUDE.md)：偏向 Claude Code / 代码工作流的协作原则

我自己在日常协作里，会反复强调这些做法：

- **默认可执行交付**：如果不是明确说“只要方案”，就尽量把结果做出来。
- **先看 skill，再动手**：命中现成 skill 就优先复用，多个命中时按最小覆盖原则选。
- **先探索，再提问**：先把事实摸清楚，再去问本来可以自己找到的东西。
- **先对齐，再执行**：执行前先摸清事实、复述目标、列计划、等确认。
- **危险操作先备份**：涉及删除、覆盖、重置、推送等高风险动作，要先讲清影响和回滚。
- **先验证，再说完成**：不靠“应该可以”，而是看实际结果是否满足需求。

如果你想把这套方式迁移到自己的环境里，这两份文件可以作为你的参考起点。

## Prompts

这些文件是我日常会反复用到的 prompt 模板：

- [`prompts/提示词优化器.md`](prompts/提示词优化器.md)
- [`prompts/概念解释器.md`](prompts/概念解释器.md)
- [`prompts/视频时间戳总结.md`](prompts/视频时间戳总结.md)
- [`prompts/论文精读.md`](prompts/论文精读.md)
- [`prompts/论文转网页.md`](prompts/论文转网页.md)

如果你只是想先快速抄作业，这一层通常是最容易马上拿去用的。

## Skills

围绕 skills，这个仓库里现在主要保留两层结构；另外，少数已经更适合单独维护的项目，我会单独拆仓：

- [`skills/`](skills)：人类可读的中文索引与技能卡片
- [`skills/full/`](skills/full)：当前适合公开同步的完整 skill 包

如果你想先看这个仓库里可直接浏览、可直接复用的 skill，我建议先看：

- [`skills/README.md`](skills/README.md)
- [`skills/full/README.md`](skills/full/README.md)

### 精选 Skills

- [`skills/paper-review-pipeline.md`](skills/paper-review-pipeline.md) / [`skills/full/paper-review-pipeline/`](skills/full/paper-review-pipeline)：论文自审、投稿前 QA、rebuttal 与审稿意见回复的总管式流程。
- [`skills/paperreview.md`](skills/paperreview.md) / [`skills/full/paperreview/`](skills/full/paperreview)：把接近定稿的 PDF 送到 `paperreview.ai` 做外部第二意见，但默认先本地 review。
- [`skills/skills-governance.md`](skills/skills-governance.md) / [`skills/full/skills-governance/`](skills/full/skills-governance)：盘点、去重、分组、治理本地 skill 集合。
- [`skills/session-recovery-codex.md`](skills/session-recovery-codex.md) / [`skills/full/session-recovery-codex/`](skills/full/session-recovery-codex)：恢复 Codex 会话现场，接着把任务做下去。
- [`skills/collaborating-with-codex.md`](skills/collaborating-with-codex.md) / [`skills/full/collaborating-with-codex/`](skills/full/collaborating-with-codex)：把第二个 Codex 会话拉进来做原型、复核或第二意见。
- [`skills/prompt-polisher.md`](skills/prompt-polisher.md) / [`skills/full/prompt-polisher/`](skills/full/prompt-polisher)：把语音转写、碎碎念和粗糙说明整理成真正可执行的 prompt。
- [`skills/writing-anti-ai.md`](skills/writing-anti-ai.md) / [`skills/full/writing-anti-ai/`](skills/full/writing-anti-ai)：去掉 AI 味，同时尽量保留原文真正想表达的立场和语气。
- [`skills/xhs-longform-private-publisher.md`](skills/xhs-longform-private-publisher.md) / [`skills/full/xhs-longform-private-publisher/`](skills/full/xhs-longform-private-publisher)：把已有 Markdown 长文和插图尽量无损地私密发布到小红书。

### 独立技能项目（Standalone Skills）

这部分收的是已经更适合单独维护、单独 star 和单独 fork 的技能项目；主仓这里继续保留总览、文章和它们之间的关系说明。

- [`paper-review-pipeline`](https://github.com/cnfjlhj/paper-review-pipeline)：从主仓里拆出的论文自审流水线，适合单独引用、单独 fork、单独继续迭代。
- [`paperreview`](https://github.com/cnfjlhj/paperreview)：从主仓里拆出的外部二审桥接仓，适合单独提交近定稿 PDF 并轮询结果。
- [`skills-governance`](https://github.com/cnfjlhj/skills-governance)：从主仓里拆出的 skill 盘点与治理工具，更适合作为独立小工具单独维护。
- [`session-recovery-codex`](https://github.com/cnfjlhj/session-recovery-codex)：从主仓里拆出的 Codex 会话恢复工具，用来把任务现场重新捞回来。
- [`collaborating-with-codex`](https://github.com/cnfjlhj/collaborating-with-codex)：从主仓里拆出的 Codex 协作桥，用来把第二个 Codex CLI 会话接进当前工作流。
- [`xhs-note-creator`](https://github.com/cnfjlhj/xhs-note-creator)：从主仓里拆出的小红书笔记生产线，更适合单独 fork 回去改模板、主题和发布链路。
- [`prompt-polisher`](https://github.com/cnfjlhj/prompt-polisher)：从主仓里拆出的 prompt 整理仓，适合把语音转写、碎碎念和粗糙说明先打磨成真正可执行的输入。
- [`writing-anti-ai`](https://github.com/cnfjlhj/writing-anti-ai)：从主仓里拆出的双语写作修订仓，用来去掉常见 AI 痕迹，同时尽量保留作者原本的语气和立场。
- [`xhs-longform-private-publisher`](https://github.com/cnfjlhj/xhs-longform-private-publisher)：从主仓里拆出的小红书长文私密发布仓，更适合忠实搬运已有 Markdown 长文并按顺序插入配图。

仓库内完整目录见：[`skills/README.md`](skills/README.md) / [`skills/full/README.md`](skills/full/README.md)

## 仓库结构

- [`docs/`](docs)：主文章与配图
- [`prompts/`](prompts)：可以直接拿去改的 prompt 模板
- [`skills/`](skills)：中文技能卡片与总览入口
- [`skills/full/`](skills/full)：公开版完整 skill 包
- [`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md)：我自己长期迭代的协作守则

## 说明

- 这是一个**中文优先**的仓库；目前提供了一个轻量英文入口页：[`README.en.md`](README.en.md)。
- 这里公开的是我认为适合分享、适合同步到 GitHub 的版本，不等于我本地所有私有环境配置的完整镜像。
- 目前已经拆出的独立技能项目见上；后面如果还有 skill 长成了更完整的项目，我会继续单独拆仓维护，主仓这里优先保留总览、方法论和入口。
