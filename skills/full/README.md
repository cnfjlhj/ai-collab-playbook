# 公开版 Skills（完整包）

[中文] | [English](README.en.md)

这里收的是当前适合公开同步到 GitHub 的完整 skill 包。大多数目录至少包含 `SKILL.md`，有些还会附带 `references/`、`scripts/`、`assets/` 或额外 `README.md`。

它不是我本地全部 skill 的镜像，而是我认为现在适合公开、也适合别人阅读和复用的那一部分。

## 怎么看这一层

- 如果你想回到主仓首页，看 [`../../README.md`](../../README.md) 或 [`../../README.en.md`](../../README.en.md)。
- 如果你想直接看 skill 的正文，就进入对应目录，优先读 `SKILL.md`。
- 这一级目录就是当前仓内公开的完整 skill 包目录。

## 研究与写作

- [`academic-paper-helper/`](academic-paper-helper/)：面向 AI/ML 论文写作的 LaTeX、BibTeX 与结构模板支架，更像写作辅助与片段库，而不是自动研究系统。
- [`paper2html/`](paper2html/)：把论文 PDF、arXiv/OpenReview 页面或本地 LaTeX source 转成中文 HTML 精读页，强调证据边界、KaTeX 公式、图表映射与发布前验证。
- [`paper-review-pipeline/`](paper-review-pipeline/)：面向 ML 顶会论文的本地审阅总管，把分章节审阅、问题分级、引用完整性检查与 rebuttal 流程收口在一起。
- [`paperreview/`](paperreview/)：面向 `paperreview.ai` 的提交与轮询客户端，核心是“上传 PDF → 拿 token → 轮询结果”的外部第二意见流程。
- [`question-refiner/`](question-refiner/)：在真正进入深度研究之前，用一系列澄清问题把模糊问题收敛成结构化研究任务说明。
- [`writing-anti-ai/`](writing-anti-ai/)：根据常见 AI 写作模式做风格修订，目标是去掉套路感，而不是包装成“万能规避器”。
- [`timestamped-video-summary/`](timestamped-video-summary/)：把带时间戳的字幕整理成严格结构的中文纪要，并在需要时导出 PDF。

## 协作、规划与恢复

- [`proactive-explorer/`](proactive-explorer/)：把“先摸清事实，再决定下一步”的主动探索原则固化成工作纪律。
- [`all-plan/`](all-plan/)：轻量的多视角规划入口，强调 `designer + inspiration + reviewer` 的多轮计划与纠偏。
- [`human-machine-brainstorm/`](human-machine-brainstorm/)：偏 CCB 生态的人机协同需求对齐工作流，不是泛化到任何环境的万能头脑风暴器。
- [`spec-first-mvp/`](spec-first-mvp/)：给兴奋态点子加一个小闸门，先写 `spec seed`，再做 throwaway MVP probe，再决定是否进入完整设计或实现。
- [`prompt-polisher/`](prompt-polisher/)：把语音转写、碎笔记和粗糙说明清洗成更适合 Claude 4.x 系列执行的 prompt。
- [`session-recovery-codex/`](session-recovery-codex/)：按 `session id` 或最近会话列表恢复 Codex 上下文，提取任务、TODO、文件与报错。
- [`skill-creator/`](skill-creator/)：把个人工作流沉淀成 skill 的方法论与工具包，覆盖 frontmatter、资源拆分、初始化与校验。
- [`skill-governance-loop/`](skill-governance-loop/)：从真实 case 出发做 skill 质量审计、版本更新、保留 / 禁用 / 归档决策，并明确什么应进入 `AGENTS.md`、什么应保留在 skill。
- [`skills-governance/`](skills-governance/)：以真实文件系统扫描结果为准，做技能盘点、去重、保留 / 禁用 / 归档建议。
- [`find-skills/`](find-skills/)：先查 skills.sh，再用 GitHub 深搜兜底，帮助找到合适 skill 或决定是否需要自己造一个。

## 多模型协作

- [`collaborating-with-claude/`](collaborating-with-claude/)：把 Claude Code CLI 作为第二意见来源接进当前工作流，强调桥接脚本、`SESSION_ID`，并在需要代码改动时要求 diff patch 输出。
- [`collaborating-with-codex/`](collaborating-with-codex/)：把第二个 Codex CLI 会话接进来做原型、调试或复核，但最终责任仍由当前会话承担。
- [`collaborating-with-gemini/`](collaborating-with-gemini/)：面向 Gemini CLI 的协作桥，补足对照验证与多视角协作。

## 发布与内容生产

- [`xhs-note-creator/`](xhs-note-creator/)：从内容撰写、卡片 Markdown、主题渲染到可选发布的小红书笔记生产线。
- [`xhs-longform-private-publisher/`](xhs-longform-private-publisher/)：把已有 Markdown 长文与插图尽量无损地私密发布到小红书，强调忠实搬运而不是重写。

## 备注

- 这一级目录更适合直接打开 skill 正文来看。
- 有些 skill 未来可能继续打磨，并在条件成熟后拆成更适合单独传播的独立仓。
