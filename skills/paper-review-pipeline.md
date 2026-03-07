# 论文评审流水线

对应本地 skill：`paper-review-pipeline`

适用场景：论文基本写完后的自查、投稿前 QA、camera-ready 检查、rebuttal / review response

输入：
- 论文正文或 LaTeX 段落
- 可选 PDF
- 目标会议 / 赛道
- 一句话贡献点

输出：
- 分章节 review
- P0 / P1 / P2 问题清单
- 对应修改建议

核心要求：
- 不编造引用
- 不擅自改技术含义
- 改 LaTeX 时不破坏 `\cite{}`、`\ref{}`、`\label{}`、数学环境、图表与参考文献钩子
- 盲审阶段避免暴露身份信息

补充规则：
- 如果输入是接近定稿的 PDF，先做本地 review，再额外问一次：是否还要走 `paperreview` 做外部二审
- 不自动提交到外部服务
