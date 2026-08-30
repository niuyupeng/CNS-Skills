# 综述检索披露第五轮独立保持集评测（R5，2026-08-30）

> **历史失败记录与 R5 当轮修复快照并存。** 下文保留 R5 首次黑盒运行的 **5/20**，以免抹去缺陷；其后的 20/20、105/105 和 178/178 是 R5 修复完成时的冻结快照。后续 R6 初测与修复后状态分别见 [R6 独立保持集评测](review-search-sixth-round-evaluation-2026-08-30.md) 和 [R6 修复后复评](review-search-sixth-round-reevaluation-2026-08-30.md)。

## 修复后状态（R5 当轮快照）

- 20 条冻结 R5 已全部接入数据驱动回归，完整类型、披露模式、evidence、缺失项、诊断 code/level 和 strict 方向为 **20/20**。
- 一名未参与修复的审查者逐条复核 gold，结论为 **必须修改 0/20、阻塞 ID 0**；另一轮 CLI 黑盒复核为 **400/400 原子字段、20/20 strict 方向**。
- H、R2、R3、R4 与 6 条发布红队探针在该快照中无回退；当时综述检索两模块为 **105/105**，完整测试套件为 **178/178**。
- 该 R5 快照中的 `scripts/review_search_audit.py` 为 1010 行，SHA-256 `23C68A30147D1A475B56248CD5DE818DAC3FA5D2CDC32D1D2D1E8A2109FC19E2`；数据驱动测试为 247 行，SHA-256 `850B9DDBC16CA2D765E8DA84053683C9CB119BCA6DBA471AA8633259B5FE45B3`。
- R5 gold 保持冻结时的 20 行与 SHA-256 `3EAA6DDB547F95AA417AB0E0C42E9D7B4180AFCA81E16262D10E8AD372FB861E`，没有为了迁就实现而修改预期。

修复覆盖组合式主体绑定、跨两句正负指代、表题/指南名与历史计划的文体隔离、材料/患者字段碰撞、中文 supplement 当前/未来/缺失状态，以及中英文来源角色。结果仍只是这些公开对抗案例的确定性回归，不是自然稿件上的准确率或可复现性证明。

> **阅读边界：** 以下“结论”至文末保留的是修复前首次评测快照；其中“当前实现”仅指当时 SHA-256 为 `6A87BAC7E25DAEC8B465D9251C5A5B4BADB726A222AEFEB633F6AB533BD4EDAF` 的实现。该段落中的“未修改”和“尚未加入回归”也只描述首次独立评测任务，不描述本页上方列出的修复后版本。

## 结论

20 条 R5 组合式难例在运行审计器前已冻结完整 gold。随后每条均通过实际 CLI 以 `--strict-systematic --shareable --json` 黑盒运行，并逐项比较类型、披露模式、完整 evidence、缺失元素、诊断 code/level 和 strict 退出码。

- **全字段严格通过：5/20（25.0%）**，通过项为 R5-08、R5-09、R5-10、R5-13 和 R5-16。
- **原子字段：350/400（87.5%）**。每例比较 20 个输出字段；strict 退出码不计入这 20 个字段，而是单列。
- **strict 退出方向匹配：13/20（65.0%）**。
- **strict 假接受：4 条**（R5-11、R5-12、R5-14、R5-15）。这些错误把应返回 3 的不完整系统综述返回为 0。
- **strict 假拒绝：3 条**（R5-04、R5-05、R5-07）。这些错误把应返回 0 的案例返回为 3。
- **退出方向偶然一致但全字段失败：8 条**（R5-01、R5-02、R5-03、R5-06、R5-17、R5-18、R5-19、R5-20）。前三条只是因为仍残留至少一个缺失项而碰巧保持拒绝；后五条属于 strict 不阻断的叙述综述，退出 0 不能弥补字段错误。
- 只有 **5/20** 同时满足“全字段一致”和“strict 方向一致”。其中 R5-08—R5-10 是未支持 review 类型，退出 0 表示门禁未适用，不是方法学接受。

因此，修复前实现仍只适合作为带明确免责声明的结构分诊工具。R5 暴露了会改变 strict 方向的安全性缺陷；不能把已知 H/R2/R3/R4 回归全过、R5 的原子字段高分或任何单次退出码 0 解释为真实综述上的普遍有效、检索可复现、符合报告指南或投稿就绪。

## 冻结与黑盒协议

### 冻结顺序

1. 完整读取项目恢复档案、`SKILL.md`、当前 `scripts/review_search_audit.py`，以及 H、R2、R3、R4 案例和历史评测。
2. 设计 20 条不依赖简单词形替换的 R5 难例，并为每条预先写定：
   - `expected_declared_type`；
   - `expected_disclosure_pattern`；
   - 完整 `expected_evidence`；
   - `expected_missing_systematic_elements`；
   - diagnostic code 与 level；
   - `expected_strict_exit`；
   - 人工判断理由。
3. 在任何 R5 CLI 调用前写入并校验 `evals/review-search-fifth-round-cases.jsonl`。冻结时为 20 行、20 个唯一 ID，SHA-256 为 `3EAA6DDB547F95AA417AB0E0C42E9D7B4180AFCA81E16262D10E8AD372FB861E`。
4. 冻结后不修改 gold。每例写入工作区外的独立临时 TXT，实际调用：

```text
py -3.11 scripts/review_search_audit.py <case.txt> --strict-systematic --shareable --json <report.json>
```

5. 逐字段比较 JSON，并记录进程退出码。40 个临时输入/输出文件在确认位于系统临时目录后全部清除。

### 评测快照

- 审计器：`scripts/review_search_audit.py`，847 行，版本 `0.8.0`，SHA-256 `6A87BAC7E25DAEC8B465D9251C5A5B4BADB726A222AEFEB633F6AB533BD4EDAF`。
- R5 gold：`evals/review-search-fifth-round-cases.jsonl`，20 行，SHA-256 `3EAA6DDB547F95AA417AB0E0C42E9D7B4180AFCA81E16262D10E8AD372FB861E`。
- 首次独立评测任务未修改核心脚本、`SKILL.md`、`references/`、现有测试或既有 eval。
- 既有 H/R2/R3/R4 回归复核：

```text
py -3.11 -m unittest tests.test_review_search_audit tests.test_review_search_forward_cases -v
Ran 78 tests
OK
```

78/78 只说明既有固定案例没有回退，不是自然稿件分布上的准确率。

## 全字段计分方法

每例的 20 个原子字段为：

1. `declared_review_type`；
2. `disclosure_pattern`；
3. `named_databases`；
4. `discovery_or_verification_sources`；
5. `source_roles_explicit`；
6. `search_context_paragraphs`；
7. `search_date_or_cutoff`；
8. `keyword_inventory`；
9. `executable_query_markers`；
10. `supplementary_search_record`；
11. `supplementary_search_status`；
12–17. selection 的 eligibility、selection logic、deduplication、screening、flow accounting、version handling；
18. `coverage_boundary_paragraphs`；
19. `missing_systematic_elements` 完整有序列表；
20. diagnostics 的 code/level 完整有序列表。

“全字段严格通过”要求 20/20。`expected_strict_exit` 单独计分，因为同一退出方向可能掩盖字段错误或类型门禁未适用。

## 逐案结果

| ID | 组合式对抗点 | 字段 | strict 预期→实际 | 主要差异或解释 |
|---|---|---:|---:|---|
| R5-01 | 中文同段分号/破折号；临床病例与文献主体并置 | 17/20 | 3→3 | 病例记录去重和筛选被误作书目去重/筛选；仅因 flow 仍缺而方向偶然正确。 |
| R5-02 | 英文破折号明确排除 search export；聚合物候选库流程 | 18/20 | 3→3 | 候选库 flow 被误作文献 flow；dedup/screening 仍缺，故方向偶然正确。 |
| R5-03 | 跨两句 `They` 回指电子病历 | 18/20 | 3→3 | 电子病历 flow 被误作文献 flow；其余两项被正确排除，故方向偶然正确。 |
| R5-04 | 跨两句 `They` 明确回指书目导出（正对照） | 16/20 | 0→3 | 真正的书目 deduplication 被漏报，导致 incomplete、critical 和 strict 假拒绝。 |
| R5-05 | 未加引号的表题含 `This Systematic Review` | 16/20 | 0→3 | 表题覆盖本文先前 narrative 自指，误升 systematic 并触发 7 项缺失。 |
| R5-06 | 中文外部指南名含“本系统综述” | 19/20 | 0→0 | 类型判断正确，但自然中文“未声称穷尽全部研究”未计入覆盖边界；方向一致不代表字段完整。 |
| R5-07 | 中文历史 systematic 计划撤回；最终 realist | 16/20 | 0→3 | 已撤回且未实施的计划压过最终未支持文体，误判 systematic。 |
| R5-08 | 历史 scoping 方案被取代；最终 living review | 20/20 | 0→0 | 全字段一致；living 仍是未支持类型，0 表示门禁未适用。 |
| R5-09 | Evidence mapping review，系统式结构齐全 | 20/20 | 0→0 | 全字段一致；mapping 未进入 strict 类型本体，0 不是方法学接受。 |
| R5-10 | Realist review，方法结构明显不完整 | 20/20 | 0→0 | 全字段一致；realist 未进入 strict 门禁，所以不完整也返回 0。 |
| R5-11 | `MH` 与材料数据库的 material-history 字段同名 | 16/20 | 3→0 | 材料字段被误作 MEDLINE 查询，升级为 structurally complete，strict 假接受。 |
| R5-12 | `TITLE-ABS-KEY` 与患者复合临床变量同名 | 16/20 | 3→0 | 临床变量被误作 Scopus/PubMed 查询信号，strict 假接受。 |
| R5-13 | 中文当前随稿 supplement | 20/20 | 0→0 | 当前存在、逐库式和运行日期均正确识别；仍只代表文本结构信号。 |
| R5-14 | 中文 future supplement：尚在整理、以后上传、当前未附 | 15/20 | 3→0 | 未来附件被反向识别为 `claimed_present`，造成 strict 假接受。 |
| R5-15 | 中文明确缺失 supplement：投稿包无文件且未归档 | 15/20 | 3→0 | 明确缺失仍被识别为 `claimed_present`，造成 strict 假接受。 |
| R5-16 | 来源角色跨句但代词有竞争先行词（负对照） | 20/20 | 0→0 | 正确保守提示 publisher/DOI 角色不清。strict 对 narrative 不作接受判断。 |
| R5-17 | 英文跨两句明确重复 `Those platforms/pages`（正对照） | 18/20 | 0→0 | 两个清楚角色均漏报并产生角色诊断；0 仅因 narrative 不阻断。 |
| R5-18 | 自然中文跨两句“前述平台/上述页面” | 16/20 | 0→0 | 两个明确角色及覆盖边界漏报，透明范围降为 partial；0 仍是非阻断方向。 |
| R5-19 | 同句破折号明确排除发现角色 | 16/20 | 0→0 | publisher 全文角色和选择逻辑漏报，产生角色诊断；DOI 角色识别正确。 |
| R5-20 | 中文破折号+分号概念库存，并明说不是可运行式 | 18/20 | 0→0 | inventory、非 executable 和诊断均正确；自然中文选择逻辑漏报，使 transparent 降为 partial。 |

## strict 安全性分析

### 4 条假接受

1. **R5-11：材料数据库字段碰撞。** `MH "shape memory"` 在句内已定义为 hydrogel batch 的 material-history 字段，但 `queried using` 加合法字段外形足以令其成为 executable query。
2. **R5-12：临床变量碰撞。** `TITLE-ABS-KEY` 在患者数据库中明确是 title、abscess status、kidney injury 形成的复合变量，仍被当作数据库检索式。
3. **R5-14：未来中文附件。** “尚在整理”“定稿后才会上传”“当前文件未附”都没有阻止 `补充表 + 检索式` 被识别为当前附件。
4. **R5-15：明确缺失中文附件。** “投稿包中并无该文件”“没有归档”仍被反向升级为 `claimed_present`。

这四条都把 gold 的 `systematic_record_incomplete` 改成 `systematic_record_structurally_complete`，删除缺失项和 critical 诊断，并把退出码从 3 改为 0，属于发布边界中的 P0 风险。

### 3 条假拒绝

1. **R5-04：两句以上书目共指漏召回。** `They` 明确回指 bibliographic search exports，但 deduplication 未被绑定到书目主体。
2. **R5-05：表题误作本文类型。** 后出现的表题覆盖了文章自身更早、明确的 narrative 声明。
3. **R5-07：中文历史计划误作最终类型。** “原拟”“随后撤回”“均未实施”没有阻止旧 systematic 标签进入 strict 门禁；最终 realist 文体反而被忽略。

### 8 条方向偶然一致

- **R5-01—R5-03** 都错误吸收了至少一个临床/材料流程信号，只因还有别的系统要素未命中才继续返回 3。若真实稿件再出现一个无关的 `flow`、`deduplication` 或 `screening` 短语，方向可能翻转。
- **R5-06、R5-17—R5-20** 均有重要字段错误，但文章是 narrative/structured narrative，strict 本来就不阻断，因此退出 0 不提供安全性证据。

R5-08—R5-10 虽然全字段一致，也不能作为 strict 能力的正证据：living、mapping、realist 被保守留在 `unspecified`，其 0 退出码表示该类型没有进入 strict 检查。

## 主要泛化缺陷

### P0：字段外形和附件名词可绕过 strict

- 可执行式检测仍主要依赖 token 外形和宽泛 query cue，无法稳定区分书目数据库、材料数据库和患者数据库。
- 中文 supplement 状态精度不足。当前存在的中文附件可识别，但未来时和明确缺失会被“补充表/补充方法 + 检索式”词面反向覆盖。

### P1：科学主体在复杂句和跨句窗口中不稳定

- 同段分号/破折号中的多个主体未被完整分开：clinical cases、polymer candidates 和 bibliographic records 可共享去重、筛选或 flow 信号。
- 跨两句时，明确的书目先行词可能丢失；反过来，非书目 flow 仍可能穿透主体过滤。

### P1：文体归属仍受表题和历史计划干扰

- 未加引号的表题可冒充较晚的自指声明。
- 中文“原拟—撤回—未实施—最终为未支持类型”的时间状态没有被可靠解析。
- 未支持类型保守返回 `unspecified` 是合理边界，但 strict 也因此完全不审计其方法披露。

### P1：来源角色与自然中文召回不足

- 有竞争先行词时保持保守是正确的（R5-16），但隔一个句子后重复明确名词的英文和中文正对照仍漏报（R5-17、R5-18）。
- 破折号内的否定限定可使 publisher role 漏报（R5-19）。
- 中文自然表达中的覆盖边界和案例选择逻辑仍存在漏召回（R5-06、R5-18、R5-20）。

## 外部有效性边界

即使后来 R5 被加入回归并达到 20/20，仍不得宣称工具在真实综述上普遍有效。

1. R5 是 20 条人工构造、定向选择的困难短文本，不是随机抽取的真实综述，也不能估计现实错误率、敏感度或特异度。
2. gold 由单一评估者在固定方法学原则下制定，未进行双评估者盲标、评估者一致性分析或学科组织裁决。
3. 本轮通过 TXT 输入测试语义边界，未覆盖真实长篇 DOCX 中的表格结构、脚注、尾注、文本框、引文域、修订层、跨节共指和混合语言排版。R5-05 只是“表题文字”案例，不是 Word 表格结构测试。
4. 数据库字段和科学变量的同名空间是开放的。R5 只抽样 `MH`、`TITLE-ABS-KEY`；真实材料学、临床、软件和统计文本会产生更多碰撞。
5. 附件状态、否定、自指、来源角色和代词共指有开放式自然语言变体；继续累加正则可能同时修复召回并增加新的误报。
6. Rapid、umbrella、integrative、realist、mapping、living、state-of-the-art、critical 等类型并未被统一建模。对未支持类型返回 0 只表示 strict 未运行。
7. 结构信号无法验证附件真实存在、查询可在当前数据库界面运行、检索日期与导出一致、筛选和去重台账真实、版本处理正确，或当前 PRISMA/目标期刊指南已满足。
8. 350/400 的原子字段分数被大量容易字段抬高；4 条假接受足以否定将该百分比解释为安全门禁准确率。
9. H/R2/R3/R4 的 78/78 和未来可能的 R5 固定集全过都只证明已知表达被锁定，不构成开放域泛化证据。

最安全的产品表述仍是：该脚本报告文本中检测到的有限结构信号；人工核对真实检索式、附件、导出、筛选日志、综述类型和当前报告规范始终具有最终权威。

## 本轮写入边界

仅新增：

- `evals/review-search-fifth-round-cases.jsonl`
- `evals/review-search-fifth-round-evaluation-2026-08-30.md`

首次独立评测任务没有修改核心脚本、`SKILL.md`、`references/`、现有测试或既有 eval；当时也没有把 R5 自动加入回归，以保留该轮独立保持集的历史真实性。
