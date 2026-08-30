# 综述检索披露第六轮独立保持集评测（R6，2026-08-30）

> **历史初测快照，不是当前实现的通过率。** 本文保留冻结 gold 在修复前的
> 3/12 全字段、201/240 原子字段和 7/12 strict 结果；修复后的同一金标准复评见
> review-search-sixth-round-reevaluation-2026-08-30.md。初测数字不得被回写或用修复后数字取代。

## 结论

R6 是一次先冻结 gold、后调用真实 CLI 的未知保持集评测。12 条组合式难例在任何 R6 脚本运行前已写定完整 20 个原子字段、diagnostic code/level 和 strict 退出码，冻结后没有修改 gold。

- **全字段严格通过：3/12（25.0%）**，为 R6-04、R6-05 和 R6-09。
- **原子字段：201/240（83.75%）**。每例比较 20 个输出字段；strict 退出码另列，不纳入 20 字段。
- **strict 退出方向匹配：7/12（58.3%）**。
- **strict 假接受：1 条**（R6-06），应返回 3 的不完整系统综述实际返回 0。
- **strict 假拒绝：4 条**（R6-02、R6-03、R6-07、R6-08），应返回 0 的案例实际返回 3。
- **退出方向偶然一致但全字段失败：4 条**（R6-01、R6-10、R6-11、R6-12）。R6-01 仍有其他缺失项而保持拒绝；后三条是非阻断的叙述综述，退出 0 不能弥补字段错误。

R6-04 和 R6-05 虽全字段通过，但 critical review 和 state-of-the-art review 属当前未支持类型；其 strict 退出 0 只表示类型门禁未适用。R6-09 是本轮唯一一条同时进入受支持类型门禁且全字段正确的案例。

因此，已知 H/R2/R3/R4/R5 回归全过不能被解释为开放域泛化能力。R6 暴露了新的 strict 方向错误，包括会造成假安全的字段碰撞。当前脚本仍只适合作为带明确免责声明的文本结构分诊工具，不是可复现性、附件真实性或报告合规性判定器。

## 冻结与黑盒协议

### 冻结顺序

1. 完整读取项目恢复档案、`SKILL.md` 以及 H、R2、R3、R4、R5 的 81 条既有案例。
2. 设计 12 条与既有表达不重复的组合式难例，同时放入正对照、负对照和未支持类型边界。
3. 在任何 R6 CLI 调用前写入 `evals/review-search-sixth-round-cases.jsonl`，并校验为 12 行、12 个唯一 ID、所有必需 gold 字段齐全。
4. 冻结时 gold SHA-256 为 `6C1E885A701BA2EC05798615A5864566ADE005055059BC356FE76667C3E44793`，大小为 17,358 字节。黑盒运行结束后复核哈希未变。
5. 每条案例写入系统临时目录中的独立 TXT，通过真实子进程调用：

```text
py -3.11 scripts/review_search_audit.py <case.txt> --strict-systematic --shareable --json <report.json>
```

6. 从 JSON 报告比较 20 个原子字段，并独立记录真实进程退出码。临时目录在评测进程结束时自动清理。

### 评测快照

- 审计器：`scripts/review_search_audit.py` v0.8.0，1,010 行。
- 审计器运行前与运行后 SHA-256 均为 `23C68A30147D1A475B56248CD5DE818DAC3FA5D2CDC32D1D2D1E8A2109FC19E2`。
- R6 gold：`evals/review-search-sixth-round-cases.jsonl`，12 行，SHA-256 `6C1E885A701BA2EC05798615A5864566ADE005055059BC356FE76667C3E44793`。
- 本任务未修改核心脚本、`SKILL.md`、`references/`、`tests/` 或任何既有 eval。

## 20 个原子字段

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
19. `missing_systematic_elements` 的完整有序列表；
20. diagnostics 的 code/level 完整有序列表。

“全字段严格通过”要求 20/20；`expected_strict_exit` 单独计分，因为同一退出方向可能遮蔽字段错误，或只表示类型门禁未适用。

## 逐案结果

| ID | 新组合式对抗点 | 字段 | strict 预期→实际 | 主要差异或解释 |
|---|---|---:|---:|---|
| R6-01 | 中文破折号明确排除题录；标本条码/切片主体 | 18/20 | 3→3 | 切片 screening 被误作文献 screening，并从缺失项中删除 `screening_process`；仍因 dedup/flow 缺失而偶然拒绝。 |
| R6-02 | 跨段 `citation files`→`this bibliographic set` 正对照 | 15/20 | 0→3 | `Reports were eligible when...` 未被识别为 eligibility；明确作用于 bibliographic set 的 deduplication 也漏报，造成假拒绝。 |
| R6-03 | 未加引号的外部编辑评语；作者明确拒绝该类型 | 15/20 | 0→3 | 编辑评语中的 `This systematic review` 覆盖了本文最终 structured narrative 自指，误触发系统门禁和 7 项缺失。 |
| R6-04 | 已取消 meta-analysis 注册；最终 critical review | 20/20 | 0→0 | 全字段正确；critical review 仍是未支持类型，0 只表示门禁未适用。 |
| R6-05 | state-of-the-art review 方法信号齐全 | 20/20 | 0→0 | 方法字段提取正确；未支持类型保守输出 `unspecified`。 |
| R6-06 | Ovid `.tw.` 与流变仪 torque-weighted 同形碰撞 | 16/20 | 3→0 | 明确属于流变仪并明说不是 bibliographic field 的 `hydrogel*.tw.` 仍被识别为可执行检索式，误升为 structurally complete。 |
| R6-07 | 通过显式指针跨段绑定 Scopus `TITLE-ABS-KEY/W/3` | 15/20 | 0→3 | 检索式绑定正确，但 eligibility 和明确的 `Search exports were deduplicated` 漏报，造成假拒绝。 |
| R6-08 | 否定未来存储；当前随稿 supplement 正对照 | 15/20 | 0→3 | `already included with this submission` 和“逐平台命令+执行日期”未被识别为当前附件，状态误为 absent，造成假拒绝。 |
| R6-09 | 正文引用但被封锁、未随稿、拟下年发布的 appendix | 20/20 | 3→3 | 正确识别为 `planned_or_placeholder`，并保持不完整系统记录的 critical 诊断。 |
| R6-10 | `author-maintained Zotero full-text library` 及跨段形成边界 | 14/20 | 0→0 | 自然同义表达未被识别为 author-curated collection；因此来源角色、4 段语境、同一进入规则和选择逻辑均漏报。 |
| R6-11 | publisher/DOI 合并成 `these resources` 后给出混合职能 | 17/20 | 0→0 | 在未区分两个来源职能时，DOI role 被过早标为 true；选择逻辑漏报，transparent 降为 partial。角色诊断因 publisher 仍为 false 而方向偶然一致。 |
| R6-12 | 8 项概念库；覆盖边界与发生比例推断边界并存 | 16/20 | 0→0 | 分号概念库、两类不同边界和库存诊断全部漏报，transparent 降为 partial。strict 对 structured narrative 不阻断。 |

## strict 安全性分析

### 假接受：R6-06

`hydrogel*.tw.` 具有 Ovid 字段语法的外形，但文本同句已完成三层排除：

1. 对象是 `rheometer export`；
2. `.tw.` 被就地定义为 `torque-weighted signal`；
3. 明确声明 `was not a bibliographic search field`。

审计器仍将其吸收为可执行检索式，从而删除 `executable_query_or_supplement` 缺失，清除 critical 诊断并把 strict 退出码由 3 改为 0。这是会造成假安全的 P0 风险。

### 假拒绝：R6-02、R6-03、R6-07、R6-08

1. **R6-02 和 R6-07：** `Reports were eligible when...` 这一常见纳入表达未命中；`this bibliographic set was deduplicated` 和 `Search exports were deduplicated` 两个明确书目主体也未命中。这表明上轮对跨句书目指代和选择主体的修复尚未覆盖这两类自然表达。
2. **R6-03：** 文体解析仍会将未加引号的外部编辑评语当成本文自指，即使前文已给出最终文体，后文也明确拒绝该评语。
3. **R6-08：** 附件解析识别了“未来”词面，但未理解其被 `No ... is planned` 否定，也未接受 `already included with this submission` 和具体检索命令/执行日期作为当前性正证。

### 方向偶然一致

- **R6-01** 错误吸收了切片筛选，但仍正确排除标本条码去重和流程，因而仍有两项缺失。如果真实稿件再出现一个无关 flow 或 deduplication 短语，退出方向仍可能翻转。
- **R6-10—R6-12** 是 narrative/structured narrative，strict 本来就不阻断。其各自存在 6、3、4 个原子字段错误，退出 0 不是正确披露判断的证据。

## 新暴露的泛化缺口

### P0：可执行字段仍可被显式非书目语境绕过

R5 已针对 `MH` 和 `TITLE-ABS-KEY` 的材料/患者字段碰撞进行修复，但 R6 用 `.tw.` 和新的流变仪主体表达即再次绕过 strict。这说明问题不是某两个 token，而是尚未建立稳定的“检索平台—命令—书目对象”绑定。

### P1：文献选择主体的正负识别仍不对称

- 非书目的切片 screening 可被错误吸收（R6-01）。
- 真实书目对象的 eligibility 和 deduplication 反而漏报（R6-02、R6-07）。

这种不对称会同时产生假充足和假缺失，单靠添加局部排除词很难稳定解决。

### P1：文体归属对外部评语的防护仍不完整

已有回归覆盖引号内题名、表题、指南名、旧方案和第三方旧标签，但一条未加引号、句法上归属编辑且被作者明确否定的评语，仍可覆盖最终自指。

### P1：附件时态解析对否定作用域不稳定

R6-09 能识别“引用但封锁/未随稿/拟下年发布”，但 R6-08 不能识别“不计划未来存储，因为已随稿”。当前附件存在性还会受局部未来词面影响，未稳定建模否定作用域和因果关系。

### P1：叙述综述自然表达的召回仍偏低

- `author-maintained Zotero full-text library` 未进入 author-curated collection 边界（R6-10）。
- 合并来源的混合职能被部分过度明确化（R6-11）。
- 破折号+分号的概念库和“覆盖边界—发生比例推断边界”均漏报（R6-12）。

这些失败对当前生物材料综述尤其相关：脚本可能将诚实的结构化叙述性披露降为 partial，也可能漏掉用户原段中的“非穷尽性”与“不推断领域发生比例”两种不同功能。

## 外部有效性边界

1. R6 只有 12 条人工构造、定向选择的短文本，不是真实综述的随机样本，不能估计现实错误率、敏感度或特异度。
2. gold 由单一评估者依据预先锁定的文体和报告原则制定，没有双评估者盲标、一致性分析或学科组织裁决。
3. 本轮通过 TXT 测试语义边界，没有覆盖真实长篇 DOCX 的表格结构、脚注、尾注、文本框、修订层、跨节指代或混合语言版式。
4. R6-03 是“编辑评语的纯文本”，不是 Word 批注、修订或决定信元数据的结构性测试。
5. 字段形状与科学变量的同名空间是开放的；R6 只新增 `.tw.` 一个样本，无法列举真实材料学、临床、软件和统计文本中的所有碰撞。
6. Rapid、umbrella、integrative、realist、mapping、living、critical、state-of-the-art 等类型仍未进入统一 strict 本体；对它们返回 0 只表示门禁未运行。
7. 结构信号无法验证附件真实存在、查询可在当前数据库界面重跑、检索日期与导出一致、去重/筛选台账真实，或当前 PRISMA/目标期刊指南已满足。
8. 201/240 的原子字段分数被大量容易字段抬高；1 条假接受就足以否定将该百分比解释为安全门禁准确率。
9. 未来即使将 R6 修复后纳入回归并达到 12/12，也只证明这组公开表达被锁定，不构成开放域泛化证据。

最安全的产品表述仍是：脚本仅报告文本中检测到的有限结构信号；真实检索式、附件、导出、去重和筛选日志、综述类型与当前报告规范必须由人工核对，人工判断始终具有最终权威。

## 本轮写入边界

仅新增：

- `evals/review-search-sixth-round-cases.jsonl`
- `evals/review-search-sixth-round-evaluation-2026-08-30.md`

未修改核心脚本、`SKILL.md`、`references/`、`tests/` 或任何既有 eval；本轮也没有将 R6 自动加入回归，以保留未知保持集的历史真实性。
