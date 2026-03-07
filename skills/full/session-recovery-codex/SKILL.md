---
name: session-recovery-codex
description: Use when recovering a Codex session, especially if the user provides a Codex session id or wants recent Codex sessions listed before resuming work.
---

# Session Recovery (Codex)

## 使用流程

### 分支 A：用户已经提供 session id

当用户消息里已经包含形如 `019b6d01-790f-7a32-9d75-932700db98a4` 的 session id 时：

1) 直接运行统一入口脚本：

`python3 ~/.codex/skills/session-recovery-codex/scripts/recover-session.py --id "<session_id>" --cwd "$PWD"`

2) 向用户展示脚本输出，并据此复述：
- 最后的任务请求
- 未完成事项
- 涉及文件与关键操作
- 最近报错或关键工具输出

3) 询问用户：

`我的理解是否正确？你想继续哪部分？`

### 分支 B：用户没有提供 session id

1) 运行统一入口脚本扫描当前项目最近会话：

`python3 ~/.codex/skills/session-recovery-codex/scripts/recover-session.py --cwd "$PWD" --limit 5`

2) 将脚本输出的最近 5 个会话概览展示给用户，并让用户输入要恢复的序号（1–5）。

3) 用户选择后，拿到对应 session id，再运行统一入口脚本做精确恢复：

`python3 ~/.codex/skills/session-recovery-codex/scripts/recover-session.py --id "<session_id>" --cwd "$PWD"`

4) 向用户展示：
- 最后的任务请求
- 未完成事项（TODO）（若能从 `update_plan` 记录恢复）
- 涉及的文件（若能从工具输出恢复）
- 关键决策与注意事项（从最后几条 assistant 输出提炼）

5) 询问用户：“我的理解是否正确？你想继续哪部分？”并在用户确认后继续执行任务。

## 注意事项

- 不要使用任何“压缩/精简会话”的方式替代恢复；优先用本 skill 从 `~/.codex/sessions` 恢复事实记录。
- 本 skill 现在同时覆盖“按 id 精确恢复”和“列出最近会话后再选择”两种入口。
