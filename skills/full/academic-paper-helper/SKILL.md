---
name: academic-paper-helper
description: 学术论文写作助手，专门用于 LaTeX 论文编写、BibTeX 管理、格式化、学术写作规范检查。适用于 AI/ML 研究论文、会议投稿（NeurIPS、ICML、ICLR 等）
disable-model-invocation: true
---

# 学术论文写作助手

## 功能概述

专为 AI/ML 博士生设计的学术写作助手，提供端到端的论文写作支持。

## 核心功能

### 1. LaTeX 论文框架生成

**使用场景**：创建新论文时

**模板类型**：
- **NeurIPS**：神经信息处理系统会议
- **ICML**：国际机器学习会议
- **ICLR**：国际学习表征会议
- **AAAI**：人工智能促进协会
- **CVPR**：计算机视觉与模式识别
- **ACL**：计算语言学协会
- **EMNLP**：自然语言处理经验方法会议

**生成内容**：
```latex
\documentclass{article}

% 会议特定包
\usepackage[final]{neurips_2024}  % 或其他会议

% 标准学术包
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithm,algorithmic}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}

\title{Your Paper Title}

\author{
  Your Name \\
  Department \\
  University \\
  \texttt{email@university.edu}
}

\begin{document}

\maketitle

\begin{abstract}
Your abstract here.
\end{abstract}

\section{Introduction}
% Your content

\section{Related Work}
% Your content

\section{Method}
% Your content

\section{Experiments}
% Your content

\section{Conclusion}
% Your content

\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

### 2. BibTeX 条目管理

**使用场景**：管理论文引用

**功能**：
- 从论文信息自动生成 BibTeX 条目
- 格式化作者名字（全名、首字母大写）
- 标题大小写规范（Chicago style）
- 自动添加 DOI

**示例**：

输入混乱的论文信息：
```
attention is all you need
vaswani et al
2017
neurips
```

输出规范的 BibTeX：
```bibtex
@inproceedings{vaswani2017attention,
  title={Attention Is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N. and Kaiser, {\L}ukasz and Polosukhin, Illia},
  booktitle={Advances in Neural Information Processing Systems},
  volume={30},
  year={2017},
  doi={10.5555/3295222.3295349}
}
```

### 3. 学术写作规范检查

**检查项目**：

#### 语言规范
- ✅ 使用第三人称（避免 "we", "I"）
- ✅ 使用被动语态（学术风格）
- ✅ 避免口语化表达
- ✅ 使用完整句子
- ✅ 段落逻辑连贯

#### 格式规范
- ✅ 图表编号和引用正确
- ✅ 公式编号和引用正确
- ✅ 引用格式统一（\cite{}）
- ✅ 缩写首次使用时定义
- ✅ 术语使用一致

#### 内容规范
- ✅ Abstract 长度（通常 150-250 字）
- ✅ Introduction 结构（动机 → 问题 → 贡献）
- ✅ Related Work 充分讨论
- ✅ Method 清晰可复现
- ✅ Experiments 完整（数据集、指标、对比）
- ✅ Conclusion 总结贡献和未来工作

### 4. LaTeX 编译错误诊断

**常见错误及解决**：

```latex
% 错误 1：Undefined control sequence
% 原因：包未导入或命令拼写错误
% 解决：检查 \usepackage{} 和命令名

% 错误 2：Missing $ inserted
% 原因：数学符号在文本模式中使用
% 解决：使用 $...$ 或 \( ... \) 包围数学内容

% 错误 3：File not found
% 原因：图片或 .bib 文件路径错误
% 解决：检查文件路径，使用相对路径

% 错误 4：Citation undefined
% 原因：.bib 文件未编译或引用键错误
% 解决：运行 bibtex，检查引用键
```

### 5. 论文结构模板

#### Introduction 结构

```latex
\section{Introduction}

% 段落 1：研究背景和动机
Recent advances in [field] have led to...
However, existing approaches suffer from...

% 段落 2：具体问题
Consider the problem of [specific problem]...
Current methods [limitation 1], [limitation 2]...

% 段落 3：本文方法概述
To address these challenges, we propose [method name]...
Our approach [key innovation 1], [key innovation 2]...

% 段落 4：主要贡献
The main contributions of this work are:
\begin{itemize}
    \item We propose [contribution 1]...
    \item We demonstrate [contribution 2]...
    \item We achieve [contribution 3]...
\end{itemize}
```

#### Method 结构

```latex
\section{Method}

\subsection{Problem Formulation}
Let $\mathcal{X}$ denote... We aim to learn...

\subsection{Architecture}
Our model consists of... Figure~\ref{fig:architecture} illustrates...

\subsection{Training Procedure}
We optimize the following objective:
\begin{equation}
    \mathcal{L} = \mathbb{E}_{(x,y)\sim\mathcal{D}}[\ell(f_\theta(x), y)]
\end{equation}

\subsection{Implementation Details}
We implement our method in PyTorch...
```

#### Experiments 结构

```latex
\section{Experiments}

\subsection{Experimental Setup}
\textbf{Datasets:} We evaluate on...
\textbf{Baselines:} We compare against...
\textbf{Metrics:} We report...
\textbf{Implementation:} We use...

\subsection{Main Results}
Table~\ref{tab:main_results} shows...

\subsection{Ablation Study}
To understand the contribution of each component...

\subsection{Analysis}
Figure~\ref{fig:analysis} visualizes...
```

### 6. 常用 LaTeX 代码片段

#### 算法伪代码

```latex
\begin{algorithm}
\caption{Your Algorithm}
\label{alg:youralgorithm}
\begin{algorithmic}[1]
\REQUIRE Input $x$
\ENSURE Output $y$
\STATE Initialize $\theta$
\FOR{$t = 1$ to $T$}
    \STATE Compute $\nabla_\theta \mathcal{L}$
    \STATE Update $\theta \leftarrow \theta - \alpha \nabla_\theta \mathcal{L}$
\ENDFOR
\RETURN $\theta$
\end{algorithmic}
\end{algorithm}
```

#### 表格

```latex
\begin{table}[t]
\centering
\caption{Comparison with baselines}
\label{tab:results}
\begin{tabular}{lcc}
\toprule
Method & Accuracy & F1-Score \\
\midrule
Baseline 1 & 85.3 & 82.1 \\
Baseline 2 & 87.6 & 84.5 \\
\textbf{Ours} & \textbf{91.2} & \textbf{89.3} \\
\bottomrule
\end{tabular}
\end{table}
```

#### 图片

```latex
\begin{figure}[t]
\centering
\includegraphics[width=0.8\linewidth]{figures/architecture.pdf}
\caption{Overall architecture of our model.}
\label{fig:architecture}
\end{figure}
```

#### 数学公式

```latex
% 行内公式
The loss function $\mathcal{L}(\theta)$ is defined as...

% 单行公式
\begin{equation}
    \mathcal{L}(\theta) = \sum_{i=1}^{n} \ell(f_\theta(x_i), y_i)
\end{equation}

% 多行公式
\begin{align}
    \mathcal{L}(\theta) &= \mathbb{E}_{x\sim p_{\text{data}}}[\log p_\theta(x)] \\
                        &= \sum_{i=1}^{n} \log p_\theta(x_i)
\end{align}
```

### 7. 引用风格

**正确引用方式**：

```latex
% 作为名词
\citet{vaswani2017attention} proposed the Transformer architecture.
% 输出：Vaswani et al. (2017) proposed...

% 括号中
The Transformer architecture~\citep{vaswani2017attention} has...
% 输出：... architecture (Vaswani et al., 2017) has...

% 多个引用
Recent work~\citep{vaswani2017attention,devlin2018bert} has shown...
% 输出：... work (Vaswani et al., 2017; Devlin et al., 2018) has...
```

### 8. 投稿前检查清单

#### 内容检查
- [ ] Abstract 清晰概括论文贡献
- [ ] Introduction 动机充分，问题明确
- [ ] Related Work 全面覆盖相关文献
- [ ] Method 可复现，细节充分
- [ ] Experiments 数据集、指标、对比实验完整
- [ ] Conclusion 总结贡献，讨论局限性

#### 格式检查
- [ ] 符合会议模板要求
- [ ] 页数限制（通常 8-10 页）
- [ ] 图表清晰，标题和标签正确
- [ ] 所有引用格式正确
- [ ] 缩写定义
- [ ] 无编译错误或警告

#### 语言检查
- [ ] 无语法错误
- [ ] 术语使用一致
- [ ] 避免主观表达
- [ ] 段落逻辑清晰

#### 补充材料
- [ ] 代码仓库链接
- [ ] 附录（如需要）
- [ ] 作者声明和伦理审查

## 工作流程

### 新论文创建流程

1. **选择会议模板**：确定投稿会议（NeurIPS/ICML/ICLR 等）
2. **生成框架**：使用模板创建基本结构
3. **填写内容**：按模板填写各部分
4. **添加引用**：管理 BibTeX 条目
5. **编译检查**：解决 LaTeX 错误
6. **规范检查**：运行学术规范检查
7. **投稿准备**：完成投稿前检查清单

### 引用管理流程

1. **收集论文信息**：从 Google Scholar、arXiv 等获取
2. **生成 BibTeX**：自动格式化条目
3. **添加到 .bib 文件**：整理到 references.bib
4. **在文中引用**：使用 \cite{} 或 \citep{}
5. **编译**：运行 latex → bibtex → latex → latex

## 集成 AGENTS.md / CLAUDE.md 规则

### 遵守的规则

- **主动探索**：优先搜索相关论文、模板与格式要求
- **执行门禁**：涉及改稿、重构或批量替换前，先对齐目标、范围与验收标准
- **结果验证**：BibTeX、编译、格式检查都要实际跑通再算完成

### 与其他 Skills / 工具配合

- **论文审阅类 workflow**：用于投稿前 QA 和多轮自审
- **演示文稿工具**：从论文内容整理 slides 或报告提纲
- **PDF 工具链**：从 PDF 提取文本、表格与关键内容

## 相关资源

- LaTeX 云编辑器：https://www.overleaf.com/
- BibTeX 搜索：https://scholar.google.com/
- 会议模板：https://www.overleaf.com/gallery/tagged/academic-journal
- LaTeX 符号：https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols

---

**版本**: v1.0
**创建日期**: 2025-10-21
**适用对象**: AI/ML 博士生、研究人员
**核心价值**: 提高学术写作效率，确保论文质量和规范性
