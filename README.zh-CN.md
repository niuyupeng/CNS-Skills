# CNS Skills 中文说明

**CNS = Cell · Nature · Science。**

CNS Skills 是面向 ChatGPT/Codex、Claude Code 与 Agent Skills 兼容客户端的开放科研写作 Skill：覆盖 SCI 论文英文润色、学术中译英、稿件重构、同行评审、回复审稿人、引文/DOI 核验以及论文图表与图注审计。

它以 Cell、Nature、Science 及各领域顶刊顶会的编辑与审稿标准为目标。对于 SCI 英文期刊和国际顶会，它默认把**英文投稿成稿**作为最终交付；中文用于锁定主张、证据、术语和作者决策，并可保留为关键修改说明。它不是逐句翻译器，而是先重建论证，再用目标领域的英文完成表达。

这里的 CNS 是质量标杆，不代表与 Cell、Nature、Science、相关出版社或任何顶会存在官方关系，也不承诺录用结果。没有足够实验和证据时，润色不能把工作“写成顶刊”；CNS 会明确指出需要补充的实验、分析或报告项目。

## 为什么不是普通“润色”

普通润色容易出现两类问题：一是句子变顺了，结论却被无意放大；二是模板词少了，但文章仍然没有作者自己的判断。CNS 规定了严格优先级：

> 证据完整性 > 原意保留 > 论证逻辑 > 作者声音 > 表面优美

因此，预测不会被写成发现，体外结果不会被写成临床有效，无法核实的 DOI 也不会被“补全”。

## 30 秒安装

### ChatGPT 桌面端 / Codex 插件

```bash
codex plugin marketplace add niuyupeng/CNS-Skills
```

重启 ChatGPT 桌面端，在 Plugins Directory 中选择 **CNS Skills** 来源并安装，然后新建对话。当前 GitHub 插件包可直接用于本地与仓库分发；要进入 ChatGPT/Codex 全局公共目录，仍需另行通过平台审核。

### Claude Code 插件

```bash
claude plugin marketplace add niuyupeng/CNS-Skills
claude plugin install cns-skills@cns-skills
```

Claude 可根据任务描述自动调用；显式调用命令是 `/cns-skills:cns-skills`。

### 独立 Skill 安装

ChatGPT 桌面端 / Codex 当前个人技能目录：

```bash
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.agents/skills/cns-skills
```

Claude Code 个人技能目录：

```bash
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.claude/skills/cns-skills
```

每个 GitHub Release 还提供可直接用于平台上传/审核的 `cns-skills-vX.Y.Z.zip` 及 SHA-256 校验文件；压缩包用同一套平台中立 Skill 同时封装 OpenAI 与 Claude 清单。

## 直接这样说

- “帮我润色这篇 SCI 论文，所有结论、数字和引文都不能改错。”
- “把这份中文综述重写成自然的投稿英文，不要逐句直译。”
- “像 Nature/CVPR 的 Reviewer 2 一样审这篇稿。”
- “核验 DOI、主张—引文对应关系和过度表述。”
- “完善摘要、引言和讨论，目标是顶刊投稿。”
- “设计或审计论文图、表、图注和图形摘要。”

启用隐式调用后，不必背固定提示词。仓库提供了中英文[正向与负向触发评测](evals/README.md)，检查“论文润色、中译英、审稿回复、顶刊顶会、图表审计”是否容易触发，同时避免把单纯找文献、仅改参考文献格式、普通文案、中枢神经系统知识问答或规避 AI 检测误路由到 CNS Skills；评测页面也明确说明它不代表所有宿主版本的调用保证。

## 推荐的完整提示词

```text
使用 $cns-skills 的 English-final + CNS/top-venue 模式完善这篇中文综述，目标为 Nature 系列期刊。
运行 12 项编辑门槛审查，保留原始主张和文献编号，核对 DOI、发表状态与实验验证层级，
从主张—证据图重写英文稿，不做逐句直译；重构中心论点、摘要、图表和图注，
输出英文投稿稿、中文关键修改说明和逐页检查后的 DOCX。
```

自动审计：

```bash
python scripts/cns_audit.py manuscript.docx --verify-dois --shareable --json cns-report.json
python scripts/check_invariants.py 中文源稿.docx 英文修改稿.docx --shareable --json invariants.json
python scripts/check_crossrefs.py 英文修改稿.docx --shareable --json crossrefs.json
```

脚本会提示高风险主张、数字附近缺少可识别引用、重复开头、套话、对称句式与 DOI 解析结果；还会比较中英文稿中的数字、单位、统计量、引用和图表编号，并检查图表“有引用无图注 / 有图注无引用”。它们是透明的分诊工具，不是 AI 检测器，也不能证明翻译等价或代替逐篇阅读原始文献。完整 JSON 可能包含本地路径和未发表稿件片段，应按保密文件处理；对外分享时使用 `--shareable` 去除这些字段。

## 顶刊顶会语料基线与图表能力

0.3.0 版加入、0.4.0 版继续保留了可复现的 320 篇英文摘要基线：Cell、Nature、Science、AAAI、CVPR、NeurIPS、ICML、ICLR 各 40 篇。分析器只输出聚合指标和题名/标识符清单，不保存摘要全文；会议年份覆盖差异也会明确披露。这些统计用于检查写作判断，不是照抄模板或录用预测器。

```bash
python scripts/venue_corpus_analyzer.py --per-venue 40 --seed 20260830
```

CNS 同时加入图表证据工作流：先建立图表主张账本，再检查数据来源、独立样本量、重复结构、不确定性、统计检验、坐标与分母、色觉可访问性、图注完整性和最终尺寸渲染。生成式图像只能用于期刊允许且明确标注的概念示意，绝不能生成或修改实验数据。

## 重要边界

CNS 不承诺“零 AI 率”，不帮助规避编辑部或平台检测，也不保证顶刊顶会录用。AI 检测分数缺乏稳定、可复现的科学含义。项目关注更可靠的目标：事实可核验、结论不过界、贡献说得清、关键替代解释得到处理、图表承担论证、语言符合目标领域的真实写作习惯。

完整英文文档见 [README.md](README.md)，详细工作流见 [SKILL.md](SKILL.md)。
