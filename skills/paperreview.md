# 外部论文二审

对应本地 skill：`paperreview`

适用场景：论文接近定稿后，提交到 `paperreview.ai` 做外部第二意见

输入：
- 最终版或接近最终版 PDF
- 目标会议
- 你自己的提交邮箱

输出：
- 提交 token
- 轮询后的 JSON / Markdown 评审结果

补充规则：
- 先做本地 review，再决定是否走外部二审
- `--submit` 属于真实外部副作用，默认先 `--dry-run`
- 公共版本不内置个人邮箱
独立仓库：<https://github.com/cnfjlhj/paperreview>
