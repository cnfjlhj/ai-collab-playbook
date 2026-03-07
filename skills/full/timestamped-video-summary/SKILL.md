---
name: timestamped-video-summary
description: "Generate a detailed, professional video content summary from timestamped subtitles/transcripts (e.g., lines starting with 00:00 / 1:23:45). Enforce strict per-segment structure (timestamp range + bold segment title + 2-paragraph body: first-person creator summary + expert 【导师评注】 critique with uncertainty handling). Use when the user provides time-coded subtitles and asks for a规范化纪要/内容纪要/逐段总结, and optionally wants a clean PDF export (do NOT include the full raw transcript in the PDF unless explicitly requested)."
---

# Timestamped Video Summary

## Overview

将“带时间戳的字幕/转录”整理为**严格结构**的视频内容纪要，并在用户要求“落盘/导出/PDF”时，把纪要渲染成排版清晰的中文 PDF（默认不附带原始逐行字幕材料）。

## Workflow Decision Tree

1) 只要文字纪要  
- 直接按“输出规范”生成 Markdown 纪要即可（无需落盘）。

2) 需要落盘为 PDF（排版清楚）  
- 先生成符合规范的 Markdown 纪要 → 写入 `*.md` → 运行 `scripts/validate_summary_md.py` 校验 → 运行 `scripts/render_pdf.py` 生成 `*.pdf`。

## Input Assumptions

- 输入是**带时间戳**的字幕/转录文本，典型形态为：
  - `00:00` / `00:02` / `01:23` / `1:23:45` 这样的时间戳行
  - 其下一行/多行是字幕内容
- 允许字幕存在口误、ASR 错别字、英文大小写/空格 token 等噪声；纪要要“忠实还原 + 专业归纳”，不要凭空补剧情。

## Output Spec (Strict)

对字幕的每个**逻辑段落**，输出必须包含且仅包含以下三部分（按顺序）：

1) 时间戳范围  
- 格式：`时间戳范围: [开始时间 - 结束时间]`

2) 段落核心标题  
- 紧跟时间戳范围下一行  
- 必须用 Markdown 加粗：`**标题**`  
- 标题要“精准概括该段落内容”，避免空泛（如“介绍一下”“继续讲”）。

3) 内容主体（两层，但不加额外小标题/前缀）  
- 第一段：核心内容总结（**必须**用博主第一人称：“我/我们”），忠实复述观点、论证、操作；用 **加粗**突出关键术语/核心结论/数据。  
- 第二段：另起一段，必须以 `【导师评注】` 开头；以顶尖专家口吻补充概念、指出漏洞/争议；若无法判断真伪，必须明确写出该点**“需要进一步验证”**，并给出具体验证思路/方法。

禁止项（默认规则）：
- 不要把“原始逐行字幕（每行时间戳+原文）”附在纪要或 PDF 后面（除非用户明确要求“把原字幕也附录进去”）。
- 不要在内容主体里加“核心内容总结：/导师评注：”这类额外标题；导师段只允许前缀 `【导师评注】`。

## Segmentation Heuristics (Practical)

将字幕分成“逻辑段落”时：
- 以话题切换、板书/投影片章节、例子切换、从原理→实作等自然边界为主
- 段落不要过碎（否则标题会变得重复、信息密度下降）；也不要过大（否则难以检索）
- 段落时间跨度建议落在 1–5 分钟量级；必要时可更长，但标题必须能覆盖主要内容

## Quality Checklist (Before Final)

- 每段都满足：时间戳范围 + **标题** + 两段正文（第二段以 `【导师评注】` 开头）
- 第一段是否全程第一人称（我/我们），且没有混入“导师视角”
- 关键术语/结论/数据是否用 **加粗**标出（不过度加粗）
- 导师评注是否包含：概念补充 + 批判性审视 + 不确定性处理（需要进一步验证 + 验证方法）
- 未出现“原始逐行字幕全文”

## PDF Export (No Raw Transcript Appendix by Default)

落盘流程建议：
1) 先把最终纪要写入 `output.md`
2) 运行校验：`python3 scripts/validate_summary_md.py output.md`
3) 生成 PDF：`python3 scripts/render_pdf.py --input output.md --outdir .`

命名规则（默认不覆盖）：
- 输出文件名默认形如：`视频纪要_<主题短名>_<YYYYMMDD_HHMMSS>.pdf`
- 若同名已存在：自动追加 `-v2/-v3`

## Resources

- `scripts/validate_summary_md.py`：格式与硬性规范校验
- `scripts/render_pdf.py`：把纪要 Markdown 渲染为 PDF（封面+目录+模块化段落；默认不附原字幕）
