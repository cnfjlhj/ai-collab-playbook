---
name: xhs-longform-private-publisher
description: This skill should be used when the user wants to publish an existing Markdown article to Xiaohongshu as a private longform post, keep the original wording and structure, insert inline images in order, use one-click layout, and verify the result in note manager.
version: 0.1.0
---

# 小红书长文私密发布技能

这个 skill 面向“已有原文、已有配图、不要改写、直接发布”的场景。

它的核心目标不是重新创作小红书文案，而是把现成的 Markdown 长文尽量无损地搬到小红书长文编辑器里，按图片占位顺序插图，使用“一键排版”，并默认以“仅自己可见”的方式发布，再做一次可视化验收。

如果用户要的是“帮我改写成更像小红书的风格”“帮我做封面卡片”“帮我生成图文卡片”，优先使用 `xhs-note-creator`；这个 skill 更适合“忠实发布现有长文”。

## 适用场景

- 用户说“帮我发小红书长文”
- 用户强调“不要改原文”“不要改原先样子”
- 用户要求“图片按顺序插进去”
- 用户要求“用一键排版”
- 用户要求“先私密发布，我来验收”
- 用户提供的是 `Markdown` 文件而不是最终可直接上传的图片卡片

## 输入

最少需要以下输入：

- `<markdown_path>`：原文 Markdown 文件
- `<image_dir>` 或 `<image_paths...>`：正文插图，顺序与文中的图片占位一致

常见可选项：

- 是否强制“仅自己可见”（默认是）
- 是否允许图片数量与占位数量不一致（默认不允许）
- 是否允许最多重试 3 次（默认允许）
- 是否覆盖标题（默认从 Markdown 的第一个 H1 提取）

## 输出

- 已发布的小红书长文，默认是“仅自己可见”
- 发布验收证据：至少一张笔记管理页截图
- 一个调试载荷 JSON，供重复执行或排查问题时复用

## 工作原则

1. 保留原文措辞，不自行改写。
2. 保留原始结构，包括标题层级、列表、引用、强调、分隔线。
3. 图片必须按占位顺序插入，不允许随意重排。
4. “一键排版”在正文和图片全部插完之后再点。
5. 默认发布为“仅自己可见”，不要误发公开。
6. 结果验收以创作者平台的可见页面为准，不以控制台日志为准。
7. 若版式、图片顺序或可见性不对，最多重做 3 次，每次都要更换假设，而不是机械重试。

## 推荐流程

### 1. 预检

- 确认已经登录小红书创作者平台
- 打开长文入口：`https://creator.xiaohongshu.com/publish/publish?target=article`
- 如果用户明确说“不能走代理”，不要切代理或依赖代理页面
- 如果页面上存在旧草稿或脏状态，优先新建一篇长文，而不是在未知草稿上硬改

### 2. 生成发布载荷

优先使用内置脚本把 Markdown 转成一个稳定的 JSON 载荷：

```bash
python scripts/build_payload.py <markdown_path> --image-dir <image_dir> --output /tmp/xhs_payload.json
```

这个脚本会做几件事：

- 提取第一个 H1 作为标题
- 以 Markdown 图片语法行为分界，把正文切成 `图片数 + 1` 段
- 把每一段 Markdown 转成 HTML，避免把原始 Markdown 符号直接贴进编辑器
- 对图片文件名按数字顺序排序，如 `1.png`、`2.png`、`10.png`
- 默认要求“图片数量 = 图片占位数量”

如果用户是显式给定图片路径列表，也可以改用：

```bash
python scripts/build_payload.py <markdown_path> --images <img1> <img2> <img3>
```

### 3. 在长文编辑器里插入内容

加载 `references/xhs-longform-workflow.md` 获取最新页面选择器、按钮回退策略和验收方法。

优先使用自动化脚本：

```bash
python scripts/publish_longform.py --payload /tmp/xhs_payload.json --validate-only
python scripts/publish_longform.py --payload /tmp/xhs_payload.json --publish
```

脚本默认行为：

- 使用持久浏览器目录复用登录态
- 默认目标可见性是 `仅自己可见`
- 不传 `--publish` 时只走到发布前页面，便于人工验收
- 传 `--publish` 后会在发布后自动跳转笔记管理页并截图留证

核心要求：

- 标题填到“填写标题会有更多赞哦”对应的输入框
- 正文必须进入长文富文本编辑器，而不是短描述框
- 依次插入：`part1 -> image1 -> part2 -> image2 -> ... -> partN`
- 先完成内容，再做“一键排版”

如果直接贴 Markdown 导致页面出现 `#`、`-`、`>` 等原始符号，说明插入方式错了，应改为先转换成 HTML 再插入。

### 4. 设置可见性并发布

- 确认“仅自己可见”已经开启
- 再次检查标题前缀是否正确
- 再次检查图片数量是否和预期一致
- 点击“发布”

如果用脚本执行，可通过以下参数显式控制：

```bash
python scripts/publish_longform.py \
  --payload /tmp/xhs_payload.json \
  --visibility private \
  --publish
```

除非用户明确要求公开，否则不要切成公开发布。

### 5. 发布后验收

发布后回到笔记管理页，至少确认以下几点：

- 最新一条有 `仅自己可见`
- 标题前缀和原文标题一致
- 时间戳与本次发布时间一致
- 状态显示 `审核中` 或 `已发布`

至少保留一张截图；有条件的话，再补一张编辑页或预览页截图。

## 重试策略

允许最多 3 次完整重试。

- 第 1 次：按标准流程直发
- 第 2 次：如果图片错位或版式异常，优先重新新建一篇，不在坏稿上修补
- 第 3 次：收缩自动化范围，重点人工确认“图片插入点”“一键排版”“仅自己可见”三个关键步骤

每次重试都要说明新的判断依据，例如：

- 上次是把内容插到短描述框了
- 上次图片上传后光标没有回到正确位置
- 上次点“一键排版”的时机过早

## 常见失败模式

- 误把内容填到短描述框，导致长文正文为空
- 直接粘贴 Markdown，导致原始语法暴露
- 图片顺序错位，通常是插图前后光标位置不对
- 管理页返回后先出现骨架屏或空列表，需要等待真实列表刷新
- 标题在管理页被截断，这通常是正常现象，用前缀匹配即可
- 平台按钮顺序可能漂移，按钮下标只能当“最后的已知经验”，不能当唯一事实

## 最小验收标准

满足以下四点才算交付：

1. 笔记管理页能看到最新一条笔记
2. 该条笔记带有 `仅自己可见`
3. 标题前缀与原文一致
4. 已保存至少一张截图作为证据

## 绑定资源

- `scripts/build_payload.py`：把 Markdown 和图片整理成稳定 JSON 载荷
- `scripts/publish_longform.py`：自动打开长文编辑器、插入正文与图片、执行一键排版、切换私密并做发布后验收
- `references/xhs-longform-workflow.md`：记录长文编辑器的实际流程、选择器经验和排错点

外部检索：默认不需要；这个 skill 主要基于本地上下文和实际浏览器页面工作。
