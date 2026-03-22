# AI Collab Playbook

[中文] | [English](README.en.md)

面向科研、写作、阅读和编程的 AI 协作实战手册。这里不是零散技巧清单，而是把主文章、协作守则、常用 prompts 和完整 skills 组织成一套可复用的工作流。

如果你想找的不是“AI 看起来很厉害”，而是“怎么让它真的进入日常工作”，建议先读主文章，再按需要拿走规则文件、prompt 模板和 skill 入口。

## 先从这里开始

- **第一次来，先读主文章（2026-03-20 版）**：[`docs/phd-ai-collab.md`](docs/phd-ai-collab.md)
- **如果你只想看“AI时代生存（学习）指南”这部分**：[`docs/phd-ai-collab.md#八ai时代生存学习指南`](docs/phd-ai-collab.md#八ai时代生存学习指南)
- **想直接拿可复用规则**：[`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md)
- **想找日常会复用的模板**：[`prompts/`](prompts)
- **想浏览完整 skills 索引**：[`skills/full/README.md`](skills/full/README.md)

[![博士生 AI 协作总览图](docs/figs/phd-ai-collab-overview.png)](docs/phd-ai-collab.md)

## 这次更新

这次公开版同步到 `2026-03-20`。除了正文，我也把首页最常用的几张图重新梳理了一遍：总览图之外，还有学习指南、Code Agent 框架和学习路线图三张图。想单独看图可以直接进 [`docs/figs`](docs/figs)；想连着上下文一起看，还是建议回到主文章。

## 图集速览

<table>
  <tr>
    <td align="center" width="33%">
      <a href="docs/phd-ai-collab.md#ai-learning-guide"><img src="docs/figs/phd-ai-learning-guide.png" alt="AI时代学习指南图" width="250"></a><br>
      <sub><strong>学习指南图</strong></sub><br>
      <sub>噪声很大的时候，先把自己的判断稳住。</sub>
    </td>
    <td align="center" width="33%">
      <a href="docs/phd-ai-collab.md#code-agent-framework"><img src="docs/figs/phd-ai-agent-framework.png" alt="Code Agent 协作框架图" width="250"></a><br>
      <sub><strong>Code Agent 框架图</strong></sub><br>
      <sub>我是怎么把多个模型和 agent 接进一套工作流的。</sub>
    </td>
    <td align="center" width="33%">
      <a href="docs/phd-ai-collab.md#ai-learning-roadmap"><img src="docs/figs/phd-ai-learning-roadmap.png" alt="AI时代学习路线图" width="250"></a><br>
      <sub><strong>学习路线图</strong></sub><br>
      <sub>AI 时代哪些基本功还值得补，我自己的看法。</sub>
    </td>
  </tr>
</table>

## 仓库里还有什么

- **协作守则**：[`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md)
- **Prompts**：[`prompts/`](prompts)
- **完整 Skills**：[`skills/full/README.md`](skills/full/README.md)
- **更新节奏**：公开版本通常在每周五同步；如果当周有明显改动，也可能提前更新。

## 外部转发与讨论

- **Linux.do 转发版**：<https://linux.do/t/topic/1667121>
- **小红书转发版**：<https://www.xiaohongshu.com/discovery/item/69ab040f000000001a02d99e?source=webshare&xhsshare=pc_web&xsec_token=LBModFyJ1bo4oqM2YmRbD3X0SpH1wO_Yo72JPNGieHJRo=&xsec_source=pc_share>

## 协作守则

- [`AGENTS.md`](AGENTS.md)：Codex / 通用 agent 协作守则
- [`CLAUDE.md`](CLAUDE.md)：Claude Code 协作守则

这两份文件不是摆设，就是我平时真在用的协作规则。如果你也想把 AI 接进日常工作流，建议早点看。

## Prompts

这些是我日常会反复用到的 prompt 模板：

- [`prompts/提示词优化器.md`](prompts/提示词优化器.md)
- [`prompts/概念解释器.md`](prompts/概念解释器.md)
- [`prompts/视频时间戳总结.md`](prompts/视频时间戳总结.md)
- [`prompts/论文精读.md`](prompts/论文精读.md)
- [`prompts/论文转网页.md`](prompts/论文转网页.md)

## 完整 Skills

这里直接放完整 skill 的入口，不再重复 `skills/*.md` 那层简短卡片。

- **仓内完整 skills 总目录**：[`skills/full/README.md`](skills/full/README.md)

### 已拆成独立仓的 skills

- [`paper-review-pipeline`](https://github.com/cnfjlhj/paper-review-pipeline)
- [`paperreview`](https://github.com/cnfjlhj/paperreview)
- [`skills-governance`](https://github.com/cnfjlhj/skills-governance)
- [`session-recovery-codex`](https://github.com/cnfjlhj/session-recovery-codex)
- [`collaborating-with-codex`](https://github.com/cnfjlhj/collaborating-with-codex)
- [`xhs-note-creator`](https://github.com/cnfjlhj/xhs-note-creator)
- [`prompt-polisher`](https://github.com/cnfjlhj/prompt-polisher)
- [`writing-anti-ai`](https://github.com/cnfjlhj/writing-anti-ai)
- [`xhs-longform-private-publisher`](https://github.com/cnfjlhj/xhs-longform-private-publisher)

其余还留在本仓的完整 skills，可以直接从 [`skills/full/README.md`](skills/full/README.md) 进入。

## 说明

- 这里公开的是我愿意同步到 GitHub 的版本，不是我本地私有环境的完整镜像。
- 主仓优先保留文章、守则和完整 skill 入口；更适合单独维护的 skill，会继续拆成独立仓。

## ⭐ Star History

<a href="https://www.star-history.com/?repos=cnfjlhj%2Fai-collab-playbook&type=date&legend=top-left">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://api.star-history.com/image?repos=cnfjlhj/ai-collab-playbook&type=date&theme=dark&legend=top-left"
    />
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://api.star-history.com/image?repos=cnfjlhj/ai-collab-playbook&type=date&legend=top-left"
    />
    <img
      alt="Star History Chart"
      src="https://api.star-history.com/image?repos=cnfjlhj/ai-collab-playbook&type=date&legend=top-left"
    />
  </picture>
</a>
