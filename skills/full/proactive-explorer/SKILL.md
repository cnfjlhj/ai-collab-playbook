---
name: proactive-explorer
description: 落实 CLAUDE.md / AGENTS.md 中的“主动探索”原则，在向用户提问前自动使用 Grep、Read、Bash、WebSearch 等工具获取信息
---

# 主动探索器

## 功能说明

此 Skill 落实 CLAUDE.md / AGENTS.md 中“主动探索”原则的核心理念：
> 宁可多做 10 步探索，不让用户回答 1 个本可自己找到答案的问题。

## 核心原则

### 触发条件
收到任何任务请求时

### 强制执行流程
1. **先尽最大努力自己获取信息**（Grep、Read、Bash、WebSearch）
2. **只有在所有探索手段都已尝试后才向用户提问**
3. **提问是最后手段，不是第一反应**

## 探索工具优先级

### 第 1 层：基础工具（优先使用，速度快）

#### Grep - 搜索关键词
```bash
# 搜索函数定义
# pattern: "function getCwd"
# output_mode: "files_with_matches"

# 搜索配置项
# pattern: "TELEGRAM_BOT_TOKEN"
# glob: "**/*.js"
```

**使用场景**：
- 查找函数/类定义
- 查找配置项
- 查找使用示例
- 查找错误信息

#### Glob - 查找文件
```bash
# 查找所有 JavaScript 文件
# pattern: "**/*.js"

# 查找配置文件
# pattern: "**/config*.{js,json}"

# 查找测试文件
# pattern: "**/*.test.js"
```

**使用场景**：
- 按模式查找文件
- 了解项目结构
- 查找特定类型的文件

#### Read - 读取文件
```bash
# 读取完整文件
# file_path: "/path/to/file.js"

# 读取部分文件
# file_path: "/path/to/file.js"
# offset: 100
# limit: 50
```

**使用场景**：
- 查看文件内容
- 分析代码实现
- 读取配置文件
- 查看文档

#### Bash - 执行命令
```bash
# 检查 Git 状态
git status

# 列出目录内容
ls -la /path/to/dir

# 检查进程
ps aux | grep node

# 检查端口占用
lsof -i :3000

# 查看环境变量
echo $TELEGRAM_BOT_TOKEN
```

**使用场景**：
- 检查环境状态
- 运行测试
- 查看日志
- 系统诊断

### 第 2 层：MCP 工具（需要特殊能力时）

#### CLAUDE.md - 查询项目知识
CLAUDE.md 文件本身就是 Memory，包含项目规范和历史决策。直接读取：
```bash
# 查看全局 CLAUDE.md
Read file_path="~/.claude/CLAUDE.md"

# 查看项目 CLAUDE.md
Read file_path="<project>/CLAUDE.md"
```

**使用场景**：
- 查询项目特定规范
- 查询历史决策
- 查询技术选型

#### Sequential-Thinking - 复杂推理
```javascript
// 多步骤分析
// 复杂问题分解
// 探索多种可能性
```

**使用场景**：
- 复杂问题分析
- 多方���比较
- 架构决策

#### WebSearch - 网络搜索
```javascript
// 搜索技术文档
// 搜索最佳实践
// 搜索错误解决方案
```

**使用场景**：
- 查询最新技术
- 查询 API 文档
- 查询错误信息

### 第 3 层：Subagent（需要专业知识时）

```javascript
// 启动专业 agent
// 委派独立任务
// 并行执行
```

**使用场景**：
- 需要特定技术栈专业知识
- 独立子任务
- 并行处理

## 标准探索流程

### 场景 1：用户询问"这个项目用的什么数据库？"

**探索步骤**：
```bash
# 1. 先查 CLAUDE.md（项目知识）
Read file_path="CLAUDE.md"

# 2. 搜索配置文件
Glob pattern="**/config*.{js,json}"
Grep pattern="database|mongodb|postgres|mysql"

# 3. 搜索依赖
Read file_path="package.json"
# 查看 dependencies

# 4. 搜索连接代码
Grep pattern="connect.*database|createConnection"
```

**结果**：在探索过程中找到答案，无需询问用户

### 场景 2：用户要求"实现用户认证功能"

**探索步骤**：
```bash
# 1. 查询 CLAUDE.md 中的历史决策
Read file_path="CLAUDE.md"
Grep pattern="auth|login|jwt"

# 2. 检查现有代码
Glob pattern="**/auth*.js"
Read file_path="src/auth/..."

# 3. 查询依赖
Read file_path="package.json"
# 检查是否已有 passport, jwt 等

# 4. 搜索最佳实践
WebSearch query="Node.js JWT authentication 2025"

# 5. 分析架构
Read file_path="src/index.js"
# 了解项目结构

# 6. 询问用户（只在必要时）
# - 使用哪种认证方式？（JWT / OAuth / Session）
# - 是否需要第三方登录？
```

**结果**：通过探索获得大部分信息，只询问关键决策

### 场景 3：用户报告"程序崩溃了"

**探索步骤**：
```bash
# 1. 检查日志
Bash command="tail -100 logs/error.log"

# 2. 检查进程
Bash command="ps aux | grep node"

# 3. 检查最近的代码变更
Bash command="git log --oneline -10"
Bash command="git diff HEAD~1"

# 4. 搜索错误信息
Grep pattern="Error|Exception|crash"

# 5. 查询 CLAUDE.md 中的历史问题
Read file_path="CLAUDE.md"

# 6. 网络搜索（如果是新错误）
WebSearch query="[具体错误信息]"
```

**结果**：定位问题根源，提供解决方案，无需用户提供额外信息

## 探索决策树

```
收到用户请求
    ↓
问题是否明确？
    ├─ 是 → 继续
    └─ 否 → 主动探索澄清
    ↓
所需信息是否在项目中？
    ├─ 是 → 使用 Grep/Glob/Read
    └─ 否 → 使用 WebSearch
    ↓
是否需要历史上下文？
    ├─ 是 → 查看 CLAUDE.md
    └─ 否 → 继续
    ↓
是否需要环境状态？
    ├─ 是 → 使用 Bash
    └─ 否 → 继续
    ↓
是否需要复杂推理？
    ├─ 是 → 使用 Sequential-Thinking
    └─ 否 → 继续
    ↓
信息是否充分？
    ├─ 是 → 开始执行
    └─ 否 → 提问用户（最后手段）
```

## 常见探索模式

### 模式 1：功能实现前的探索

```bash
# 1. 查找相似实现
Grep pattern="类似功能的关键词"

# 2. 检查项目结构
Glob pattern="src/**/*.js"
Read file_path="src/index.js"

# 3. 查看依赖
Read file_path="package.json"

# 4. 查询最佳实践
WebSearch query="技术栈 + 功能 + best practices 2025"

# 5. 查询 CLAUDE.md 中的技术选型
Read file_path="CLAUDE.md"
```

### 模式 2：Bug 修复前的探索

```bash
# 1. 重现问题
Bash command="运行复现命令"

# 2. 查看日志
Bash command="tail -n 100 logs/*.log"

# 3. 搜索相关代码
Grep pattern="报错的函数或模块"

# 4. 查看最近变更
Bash command="git log --oneline -20"
Bash command="git diff HEAD~5"

# 5. 搜索类似问题
WebSearch query="具体错误信息"
Read file_path="CLAUDE.md"
```

### 模式 3：代码重构前的探索

```bash
# 1. 理解现有实现
Read file_path="目标文件"

# 2. 查找所有调用
Grep pattern="函数名"

# 3. 检查测试覆盖
Glob pattern="**/*.test.js"
Grep pattern="目标函数" glob="**/*.test.js"

# 4. 查询重构模式
WebSearch query="重构模式 + 具体场景"

# 5. 评估影响范围
Grep pattern="import.*目标模块"
```

## 避免过早提问

### ❌ 错误示例

```
用户：实现用户登录功能
Claude：您想使用哪种认证方式？JWT 还是 Session？
```

### ✅ 正确示例

```
用户：实现用户登录功能
Claude：
  1. [Grep] 搜索现有认证代码...
  2. [Read] 查看 package.json，发现已安装 jsonwebtoken
  3. [Grep] 搜索 JWT 使用示例...
  4. [Read] 查看 CLAUDE.md 中的历史认证决策...
  5. 发现项目已经使用 JWT 模式
  6. 开始实现登录功能（复用现有 JWT 机制）
```

## 探索质量检查

在完成探索后，问自己：

- [ ] 我是否尝试了所有可用的搜索工具？
- [ ] 我是否查看了相关的配置文件？
- [ ] 我是否查询了历史记录和文档？
- [ ] 我是否搜索了项目中的相似实现？
- [ ] 我是否上网搜索了最新的最佳实践？
- [ ] 我提出的问题是否真的无法通过探索获得？

**只有当所有答案都是"是"时，才可以向用户提问！**

## 集成 CLAUDE.md 规则

### 遵守的规则

- **核心行为准则中的主动探索**：此 Skill 的核心实现
- **用户时间最小化**：减少用户等待和认知负担
- **主动代理原则**：理解意图，主动补全信息

### 与其他 Skills 配合

- 所有 Skills 执行前都应该先使用此 Skill 探索
- 与 **sequential-thinking** 配合进行复杂分析
- 与版本控制类 workflow 配合，在探索完成后再进入提交阶段

## 性能优化

### 并行探索

当多个探索互不依赖时，并行执行：

```javascript
// 同时执行多个搜索
[
  Grep pattern="auth",
  Glob pattern="**/config*.js",
  Read file_path="package.json"
]
```

### 渐进式探索

从快速工具开始，逐步深入：

1. **快速扫描**（Grep, Glob）
2. **详细阅读**（Read）
3. **环境检查**（Bash）
4. **深度分析**（Sequential-Thinking, WebSearch）

## 相关文档

- 全局或项目级 CLAUDE.md / AGENTS.md：包含主动探索、执行门禁与验证规则
- 项目级规范文件：包含项目特定规范和历史决策
