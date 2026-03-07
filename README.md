# AI Collab Playbook

这是一个由一名在读博士生维护、以 **AI 协作实践** 为核心的个人 playbook，主要收录长期使用的 prompts、skills，以及围绕“博士生日常如何与 AI 协作”的持续更新内容。

如果你是第一次来到这个仓库，建议先从主文章读起：[`docs/phd-ai-collab.md`](docs/phd-ai-collab.md)。

## 快速导航

- **主文章（2026-03-06 版）**：[`docs/phd-ai-collab.md`](docs/phd-ai-collab.md)
- **Linux.do 讨论帖**：<https://linux.do/t/topic/1667121>
- **小红书发布版**：<https://www.xiaohongshu.com/discovery/item/69ab040f000000001a02d99e?source=webshare&xhsshare=pc_web&xsec_token=LBModFyJ1bo4oqM2YmRbD3X0SpH1wO_Yo72JPNGieHJRo=&xsec_source=pc_share>
- **AI 协作守则**：[`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md)
- **Prompts**：[`prompts/`](prompts)
- **Skills 索引**：[`skills/`](skills)
- **完整公开版 Skills**：[`skills/full/`](skills/full)

## 文章

### [作为一名在读博士生，我在日常是如何与 AI 协作的？](docs/phd-ai-collab.md)

这篇文章是目前仓库里最适合直接阅读的主内容。我把自己这些年在 **日常使用、科研阅读、科研绘图、科研写作、Code Agent 使用、复盘** 里的真实经验系统整理了一次，尽量保留实践细节，而不是只讲抽象方法论。

建议直接阅读全文：

- [`阅读全文`](docs/phd-ai-collab.md)
- [`查看配图`](docs/figs)

### 文章结构

- 前言：当同事，不当工具
- 一、日常使用：AI 作为随身顾问
  - 划词工具栏
  - OpenClaw
- 二、科研文献阅读
  - 阶段一：课题调研
  - 阶段二：文献网络分析
  - 阶段三：确定精读 → 逐篇攻克
  - 阶段四：知识整合
- 三、关于科研绘图
  - 科研绘图的三个类别
  - 策略：让 AI 写操纵 AI 的 Prompt
  - 一些实测对比
- 四、关于科研写作
  - 让 AI 多审几遍
  - 和 AI 一起写，可以，但前提是它真的理解对了
  - 沉淀不同领域的写作 skill
- 五、Code Agent
  - 工具演变
  - 复杂需求的处理流程
  - 各个模型特点
  - 我最推荐的做法
- 六、多回顾，最好定期复盘
  - Skill 不是越多越好
  - 警惕“效率幻觉”

## 我的Code Agent配置

配置在这两份文件：

- [`AGENTS.md`](AGENTS.md)：偏向 Codex / 通用 agent 协作的执行原则
- [`CLAUDE.md`](CLAUDE.md)：偏向 Claude Code / 代码工作流的协作原则

这套方法是我长期迭代下来的日常工作流，核心包括：

- **默认可执行交付**：如果不是明确说“只要方案”，就尽量把结果做出来
- **先看 skill，再动手**：命中现成 skill 就优先复用，多个命中时按最小覆盖原则选
- **先探索，再提问**：先把事实摸清楚，再去问本来可以自己找到的东西
- **先对齐，再执行**：执行前先摸清事实、复述目标、列计划、等确认
- **危险操作先备份**：涉及删除、覆盖、重置、推送等高风险动作，要先讲清影响和回滚
- **先验证，再说完成**：不靠“应该可以”，而是看实际结果是否满足需求

如果你想把这套方式迁移到自己的环境里，这两份文件都可以直接拿去改成你自己的版本。

## Prompts

这些文件是我日常会反复用到的 prompt 模板：

- [`prompts/提示词优化器.md`](prompts/提示词优化器.md)
- [`prompts/概念解释器.md`](prompts/概念解释器.md)
- [`prompts/视频时间戳总结.md`](prompts/视频时间戳总结.md)
- [`prompts/论文精读.md`](prompts/论文精读.md)
- [`prompts/论文转网页.md`](prompts/论文转网页.md)

## Skills

- [`skills/full/proactive-explorer/`](skills/full/proactive-explorer)：主动探索，先把事实摸清再动手
- [`skills/full/prompt-polisher/`](skills/full/prompt-polisher)：把凌乱输入整理成可执行 prompt
- [`skills/full/question-refiner/`](skills/full/question-refiner)：把模糊问题收敛成结构化研究任务
- [`skills/full/human-machine-brainstorm/`](skills/full/human-machine-brainstorm)：做人机协同的需求对齐与头脑风暴
- [`skills/full/all-plan/`](skills/full/all-plan)：用多视角规划复杂任务
- [`skills/full/academic-paper-helper/`](skills/full/academic-paper-helper)：处理论文写作、BibTeX、LaTeX 等细活
- [`skills/full/paper-review-pipeline/`](skills/full/paper-review-pipeline)：做论文自审、投稿前 QA 与 review pipeline
- [`skills/full/writing-anti-ai/`](skills/full/writing-anti-ai)：去掉 AI 味，修正文风
- [`skills/full/session-recovery-codex/`](skills/full/session-recovery-codex)：恢复 Codex 会话现场并继续执行
- [`skills/full/timestamped-video-summary/`](skills/full/timestamped-video-summary)：把时间戳字幕整理成结构化纪要
- [`skills/full/skills-governance/`](skills/full/skills-governance)：盘点、分组、治理本地 skill 集合
- [`skills/full/collaborating-with-claude/`](skills/full/collaborating-with-claude)：让 Claude 作为第二意见参与协作
- [`skills/full/collaborating-with-codex/`](skills/full/collaborating-with-codex)：让第二个 Codex 会话参与原型或复核
- [`skills/full/collaborating-with-gemini/`](skills/full/collaborating-with-gemini)：把 Gemini 拉进来做对照验证
- [`skills/full/find-skills/`](skills/full/find-skills)：优先寻找现成 skill，减少重复造轮子
- [`skills/full/xhs-note-creator/`](skills/full/xhs-note-creator)：生成小红书笔记素材，并保留发布工作流说明
- [`skills/full/xhs-longform-private-publisher/`](skills/full/xhs-longform-private-publisher)：把长文按私密方式发布到小红书
