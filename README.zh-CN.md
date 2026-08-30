# CNS Skills 中文说明

**CNS = Cell · Nature · Science。**

CNS Skills 面向中文与英文科研写作，以 Cell、Nature、Science 及各领域顶刊顶会的编辑与审稿标准为目标。对于 SCI 英文期刊和国际顶会，它默认把**英文投稿成稿**作为最终交付；中文用于锁定主张、证据、术语和作者决策，并可保留为关键修改说明。它不是逐句翻译器，而是先重建论证，再用目标领域的英文完成表达。

这里的 CNS 是质量标杆，不代表与 Cell、Nature、Science、相关出版社或任何顶会存在官方关系，也不承诺录用结果。没有足够实验和证据时，润色不能把工作“写成顶刊”；CNS 会明确指出需要补充的实验、分析或报告项目。

## 为什么不是普通“润色”

普通润色容易出现两类问题：一是句子变顺了，结论却被无意放大；二是模板词少了，但文章仍然没有作者自己的判断。CNS 规定了严格优先级：

> 证据完整性 > 原意保留 > 论证逻辑 > 作者声音 > 表面优美

因此，预测不会被写成发现，体外结果不会被写成临床有效，无法核实的 DOI 也不会被“补全”。

## 安装与使用

```bash
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.codex/skills/cns-skills
```

推荐提示词：

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

0.3.0 版加入了可复现的 320 篇英文摘要基线：Cell、Nature、Science、AAAI、CVPR、NeurIPS、ICML、ICLR 各 40 篇。分析器只输出聚合指标和题名/标识符清单，不保存摘要全文；会议年份覆盖差异也会明确披露。这些统计用于检查写作判断，不是照抄模板或录用预测器。

```bash
python scripts/venue_corpus_analyzer.py --per-venue 40 --seed 20260830
```

CNS 同时加入图表证据工作流：先建立图表主张账本，再检查数据来源、独立样本量、重复结构、不确定性、统计检验、坐标与分母、色觉可访问性、图注完整性和最终尺寸渲染。生成式图像只能用于期刊允许且明确标注的概念示意，绝不能生成或修改实验数据。

## 重要边界

CNS 不承诺“零 AI 率”，不帮助规避编辑部或平台检测，也不保证顶刊顶会录用。AI 检测分数缺乏稳定、可复现的科学含义。项目关注更可靠的目标：事实可核验、结论不过界、贡献说得清、关键替代解释得到处理、图表承担论证、语言符合目标领域的真实写作习惯。

完整英文文档见 [README.md](README.md)，详细工作流见 [SKILL.md](SKILL.md)。
