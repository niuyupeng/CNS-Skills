# CNS Skills 中文说明

**CNS = Claim-grounded, Natural, Scholarly（主张有据、表达自然、符合学术规范）**。

CNS Skills 面向中文与英文科研写作。它先锁定主张、证据和适用范围，再修复论证结构、段落功能与语言节奏；最后核对引用并检查生成文件。它适合综述、研究论文、基金申请、审稿回复和科研报告。

## 为什么不是普通“润色”

普通润色容易出现两类问题：一是句子变顺了，结论却被无意放大；二是模板词少了，但文章仍然没有作者自己的判断。CNS 规定了严格优先级：

> 证据完整性 > 原意保留 > 论证逻辑 > 作者声音 > 表面优美

因此，预测不会被写成发现，体外结果不会被写成临床有效，无法核实的 DOI 也不会被“补全”。

## 安装与使用

```bash
git clone https://github.com/niuyupeng/cns-skills.git ~/.codex/skills/cns-skills
```

推荐提示词：

```text
使用 $cns-skills 的 deep-review 模式完善这篇综述。
保留原始主张和文献编号，核对 DOI、发表状态与实验验证层级，
减少模板化表达但不要口语化，输出修改说明和逐页检查后的 DOCX。
```

自动审计：

```bash
python scripts/cns_audit.py manuscript.docx --verify-dois --json cns-report.json
```

脚本会提示高风险主张、数字附近缺少可识别引用、重复开头、套话、对称句式与 DOI 解析结果。它是透明的文本分诊工具，不是 AI 检测器，也不能代替逐篇阅读原始文献。

## 重要边界

CNS 不承诺“零 AI 率”，也不帮助规避编辑部或平台的检测。AI 检测分数缺乏稳定、可复现的科学含义。项目关注的是更可靠的目标：事实可核验、结论不过界、论证由作者判断驱动、语言符合目标领域的真实写作习惯。

完整英文文档见 [README.md](README.md)，详细工作流见 [SKILL.md](SKILL.md)。
