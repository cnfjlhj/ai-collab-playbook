# Prompt 润色器

对应本地 skill：`prompt-polisher`

适用场景：
- 语音转写或碎碎念太乱，直接执行会跑偏
- 需要把粗糙说明整理成可执行 prompt
- 想先补齐关键缺口，再交给模型做事

输入：
- 散乱笔记
- 语音转写文本
- 粗糙任务说明

输出：
- 清洗后的任务描述
- 缺口澄清问题
- 更适合执行的结构化 prompt

边界：
- 它更偏 Claude 4.x / Opus 4.5 / Sonnet 4.5 这类工作流
- 默认会先预览再执行，不是无脑自动把原文直接丢给模型

独立仓库：<https://github.com/cnfjlhj/prompt-polisher>
