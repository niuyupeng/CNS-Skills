<p align="center">
  <img src=".github/assets/cns-skills-hero.svg" width="100%" alt="CNS Skills：从初稿到经得起审稿的论文">
</p>

<div align="center">

## 让每一个主张都配得上它的位置。

**面向顶刊顶会审稿压力的证据优先稿件工程。**

CNS Skills 把中文或英文初稿推进为更清晰、更可辩护的英文投稿稿，并继续检查句子级润色可能遗漏的主张、引文、图表、审稿逻辑与最终文件。

[**快速安装**](#快速安装) · [**运行旗舰工作流**](#运行旗舰工作流) · [**查看硬证据**](#不是口号而是可核验资产) · [**引用 CNS Skills**](#引用-cns-skills) · [English](README.md)

[![Release](https://img.shields.io/github/v/release/niuyupeng/CNS-Skills?label=release&color=E9B44C)](https://github.com/niuyupeng/CNS-Skills/releases)
[![CI](https://github.com/niuyupeng/CNS-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/niuyupeng/CNS-Skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-0B6E69.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/standard-Agent_Skills-123B5D.svg)](https://agentskills.io/)
[![Cite](https://img.shields.io/badge/cite-CITATION.cff-7A263A.svg)](CITATION.cff)

**12 项编辑门槛 · 8 类场所配置 · 320 篇摘要可审计基线 · 64 条路由案例 · 45 项确定性测试 · 4 个透明审计器**

<sub>独立 MIT 开源项目。CNS 指 Cell · Nature · Science 这一编辑质量标杆，不表示隶属、背书或录用保证。</sub>

</div>

---

## CNS Skills 到底是什么

句子润色只是第一层。**CNS Skills 在不超出科学证据的前提下，重建整篇稿件。**

它先锁定来源、主张、数字、术语和证据范围，再处理中心论点、章节推进、投稿英文、主张—引文关系、审稿人质疑与图表叙事；在宿主支持文档渲染时，还会检查最终 DOCX/PDF。目标不是生成一篇“很像学术论文”的文字，而是让贡献更容易被编辑看见、让结论更经得起审稿、让尚未解决的风险无法被漂亮语言掩盖。

| 句子级润色通常停在这里 | CNS Skills 继续检查 |
|---|---|
| 句子更流畅 | 中心主张、广泛意义、新颖性和段落逻辑 |
| 中文逐句翻译 | 从主张图重写英文并回查中英文不变量 |
| 参考文献格式 | DOI/状态、真实支持范围、落位和证据独立性 |
| 图表更好看 | 图表承担的主张、来源、不确定性、图注和最终尺寸 |
| 文件能够打开 | 数字单位、交叉引用、修订、批注、可访问性和逐页渲染 |
| “看起来能投稿” | 审稿风险、缺失证据和目标期刊适配边界 |

> **唯一优先级：证据完整性 > 原意保留 > 论证逻辑 > 作者声音 > 表面优美。**

### 一个证据边界示例

下面是一个合成示例，不来自任何未公开稿件：

| 已有证据 | 原句 | CNS 判断 | 证据范围内的改写 |
|---|---|---|---|
| 只有一次体外实验 | “该平台能够推动临床转化。” | 临床结论超过了当前验证层级 | “该平台在体外改善了 X；其体内表现和临床价值仍待验证。” |

一次调用可以同时交付：**修改稿 · 决策/风险图 · 引文审计 · 图表 QA · 在宿主支持文档渲染时完成最终版面检查**。

## 运行旗舰工作流

上传稿件后可以直接这样说：

```text
使用 $cns-skills 的 English-final + CNS/top-venue 模式完善这篇稿件。
保留所有有依据的科学主张、数字、引文和项目专用量表。
从论证结构重建领域自然的英文投稿稿，不要逐句机械翻译。
检查过度表述、DOI/发表状态、主张—引文对应、图、表、图注和交叉引用。
分别以领域专家、方法审稿人、编辑和相邻学科读者的身份复核。
输出修改后的文件、精简决策/风险记录，并逐页检查最终版面。
```

也可以直接提出这些任务：

- “把这篇中文 SCI 初稿重写成自然投稿英文，不能改变科学结论。”
- “像严格的 Nature/CVPR Reviewer 2 一样审这篇稿。”
- “围绕一个可辩护的中心主张重构摘要、引言和讨论。”
- “逐条检查重要主张是否被对应文献真正支持。”
- “按论证缺口扩充这篇综述，不要为了凑篇数堆引用。”
- “设计或审计论文图、证据表、图注和图形摘要。”
- “写一份证据范围准确的审稿回复和 rebuttal。”

启用隐式调用后不需要背固定提示词。公开的[路由评测](evals/README.md)同时包含正向任务和容易混淆的负向任务，避免把普通翻译、单独查 DOI/PubMed、只改参考文献格式、中枢神经系统问答或 AI 检测规避误路由到本 Skill。

## 快速安装

### ChatGPT 桌面端 / Codex 插件

```bash
codex plugin marketplace add niuyupeng/CNS-Skills
```

重启 ChatGPT 桌面端，在 Plugins Directory 中选择 **CNS Skills** 来源并安装。当前仓库包可用于本地和仓库分发；进入共享全局目录仍须通过平台审核。

### Claude Code 插件

```bash
claude plugin marketplace add niuyupeng/CNS-Skills
claude plugin install cns-skills@cns-skills
```

Claude 可以根据任务自动选择 Skill；显式调用为 `/cns-skills:cns-skills`。

### 独立 Agent Skill

```bash
# ChatGPT 桌面端 / Codex
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.agents/skills/cns-skills

# Claude Code
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.claude/skills/cns-skills
```

每个 Release 都提供可上传的 ZIP 和 SHA-256 校验文件；仓库根 Skill 与生成的插件包会在 CI 中检查是否漂移。

## 不是口号，而是可核验资产

| 公开资产 | 能证明什么 | 不能证明什么 |
|---|---|---|
| [12 项 CNS 编辑门槛](references/cns-editorial-standard.md) | 一套公开的 12 维顶刊导向审查面 | 任何期刊或会议必然录用 |
| [8 类场所配置](references/venue-profiles.md) | 期刊与顶会不会被当成同一种写法 | 永久替代最新官方投稿政策 |
| [320 篇摘要聚合基线](references/venue-corpus-findings.md) | 可复现的场所语言描述 | 风格迁移语料或录用预测器 |
| [64 条中英文路由案例](evals/README.md) | 正负触发防回归 | 所有宿主都保证自动调用 |
| 30 条锁定留出集 | 降低针对已知样例堆关键词的风险 | 外部排行榜成绩 |
| [45 项确定性测试](tests) | 脚本行为和关键不变量 | 每一次文字修改都语义正确 |
| 4 个无第三方依赖审计器 | 本地、透明、可复核的分诊 | 自动代替原文精读和作者判断 |

本项目不虚构“成功率”、用户数量、引用次数、录用率或 AI 检测分数。宣传可以很强，但硬数字必须能在仓库里点开核验。

## 四个透明稿件审计器

需要 Python 3.9+，不依赖第三方包：

```bash
python scripts/cns_audit.py manuscript.docx --verify-dois --shareable --json cns-report.json
python scripts/review_citation_audit.py review.docx --shareable --json review-citations.json
python scripts/check_invariants.py 中文源稿.docx 英文修改稿.docx --shareable --json invariants.json
python scripts/check_crossrefs.py 英文修改稿.docx --shareable --json crossrefs.json
```

它们会报告高风险表述、DOI 状态、公式化/编辑脚手架模式、方括号数字引文结构、数字/单位/统计量/引文变化和断裂的图表引用。它们不会自动改稿、独立判断全文支持关系、证明翻译等价或充当 AI 检测器。未经 `--shareable` 处理的 JSON 可能包含本地路径和未发表片段，不能随意外传。

完整运行规则见 [SKILL.md](SKILL.md)。专题参考包括[英文优先双语写作](references/english-first-bilingual.md)、[综述写作](references/review-article-mode.md)、[自然学术语言](references/natural-academic-style.md)、[综述—Skill 双向迭代](references/iterative-review-development.md)、[图表与图注](references/figures-tables.md)、[科研诚信](references/scientific-integrity.md)和[场所配置](references/venue-profiles.md)。

## 引用 CNS Skills

如果 CNS Skills 帮你发现了原流程漏掉的问题，或实质性改善了论文、综述、rebuttal 与科研写作流程，请**给仓库 Star，并引用这个软件**。这两个公开信号能帮助更多研究者找到一种比通用“论文 humanizer”更重视证据的选择。

GitHub 会根据根目录 [CITATION.cff](CITATION.cff) 自动显示 **Cite this repository**。也可以直接复制：

```bibtex
@software{niu_cns_skills_2026,
  author  = {Niu, Yupeng},
  title   = {CNS Skills: Evidence-First Scientific Manuscript Revision and Quality Assurance},
  year    = {2026},
  version = {0.6.0},
  url     = {https://github.com/niuyupeng/CNS-Skills}
}
```

**[给 CNS Skills Star](https://github.com/niuyupeng/CNS-Skills)** · **[打开引用文件](CITATION.cff)** · **[下载最新版本](https://github.com/niuyupeng/CNS-Skills/releases/latest)**

## 参与项目

- 在 [Discussions](https://github.com/niuyupeng/CNS-Skills/discussions) 分享工作流或讨论设计。
- 在 [Issues](https://github.com/niuyupeng/CNS-Skills/issues) 提交可复现问题或功能建议。
- 通过 [CONTRIBUTING.md](CONTRIBUTING.md) 贡献测试、场所规则修正、语言模式或隐私安全的基准案例。
- 通过 [CHANGELOG.md](CHANGELOG.md) 查看公开演进记录。

## 名称、独立性与边界

“CNS”指 **Cell、Nature、Science** 这一关于清晰度、重要性、证据深度和跨学科表达的目标标杆。CNS Skills 是独立项目，与相关期刊、出版社、会议、OpenAI、Anthropic 或引用的开源项目不存在隶属或背书关系。

它不会伪造证据、编造引文、掩盖无依据结论、承诺送审或录用，也不提供 AI 检测规避。当现有科学内容支撑不了目标故事时，CNS 会收窄结论，并明确还缺哪些实验、分析或报告项目。

## 开源许可

[MIT](LICENSE) © 2026 Yupeng Niu.
