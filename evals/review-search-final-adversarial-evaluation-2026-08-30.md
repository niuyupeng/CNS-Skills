# 综述检索披露最终前向对抗评测（R3，2026-08-30）

> **历史阶段报告。** 下文保留 R3 修复前 **2/16** 的独立评测记录及当轮修复状态，便于追溯失败模式；当前完整状态见 [`evals/README.md`](README.md) 和后续 R4 报告。

## 修复后状态

- R3-01—R3-16 的预期类型、证据字段、缺失元素和诊断级别经第二次保守性审查后原样保留；没有为了迁就实现而放宽门禁。唯一需要澄清的是 R3-01：原文本命名 PubMed 与万方却只展示 PubMed 式，与“两个数据库检索记录完整”的理由不完全一致，因此补入万方主题检索式，预期输出不变。
- 16 条 R3 已加入 `tests/test_review_search_forward_cases.py` 的数据驱动回归，并以导入期守卫锁定为 16 个唯一、连续的 R3-01—R3-16 案例。既有 45 项 review-search 测试增加 16 项，现为 **61/61**。
- Python 3.9 与 Python 3.11 均通过 **61/61**：原 14 项基线、H01—H21、R2-01—R2-08、R3-01—R3-16 及 2 项 strict-mode 退出码测试全部通过。
- 当前 `scripts/review_search_audit.py` 为 790 行，SHA-256 `54907171672D437CA3B8705CF2AB4B5723E8C69E0AEBBBB15BE81C7F1069BF75`；数据驱动测试为 144 行，SHA-256 `39AA82C705CDC169B41A5B7C86CC09AB3FD7BC88AF34771537BB949DC344DC0A`；R3 JSONL 为 16 行，SHA-256 `FD9A96118B09FF625B58347485608AF84946C34E4AD14193E621A17D59573BAA`。
- 修复覆盖：中文“系统评价”和被动否定、引用题名/已放弃计划与最终文体的优先级、`Query concepts` 库存、`TS` 材料变量串扰、患者/仪器记录与文献对象的分离、来源角色同义表达、作者资料库边界、supplement 的当前/未来状态、倒装附件说明、互补边界句，以及 PubMed `[Majr]`/`[Publication Type]` 字段。
- 输出免责声明已进一步加固：`systematic_record_structurally_complete` **只表示检测到规定的文本结构信号**；它不验证补充文件真实存在、检索式可运行、检索或筛选记录真实、研究可复现、符合场所要求或达到投稿就绪状态。

修复后仍只应把该脚本作为透明的结构分诊工具。R3 是短文本人工对抗集，不是自然稿件总体上的准确率估计，也不能替代对真实查询、附件、筛选台账和当前报告指南的人工核验。

## 结论

在 16 个完全新鲜、未复用 H01–H21 或 R2-01–R2-08 措辞的 R3 案例上，`scripts/review_search_audit.py` 严格通过 **2/16（12.5%）**，失败 **14/16（87.5%）**。通过项为 R3-03 和 R3-13。

现有公开回归仍为 **45/45 通过**，说明 H/R2 已知表达被锁定；但 R3 暴露出明显的未见表达泛化缺陷。尤其有五条路径可让本应不完整或未被正确识别的系统综述绕过 strict 门禁：R3-01、R3-05、R3-06、R3-07、R3-10。另有两条相反路径会把结构完整的系统综述误拒为不完整：R3-11、R3-16。

因此，当前版本可继续作为带醒目免责声明的非阻断式结构分诊工具，但不应把 `--strict-systematic` 的零退出码解释为可靠通过，也不应把 `systematic_record_structurally_complete` 解释为检索可复现。

## 评测快照与写入边界

- 脚本版本：`0.8.0`
- `scripts/review_search_audit.py`：627 行，SHA-256 `13C65092A3D8BE2D3511BAF1495A3EBCFF4F49188BD52379541C878109D64C89`
- R3 案例：`evals/review-search-final-adversarial-cases.jsonl`，16 行，SHA-256 `C2DFE98946F0F86D37173FB4B16B43367F5A7075AABD5EF2189BB26FF887BCC1`
- 核心脚本、`SKILL.md`、`references/`、既有测试与既有评测均未修改。
- 本轮只新增本报告和上述 R3 JSONL；没有创建临时稿件文件。逐案运行通过导入目标脚本的 `build_report()`，对 JSONL 中每个 UTF-8 文本直接构建报告并逐字段比较。

现有回归复核命令：

```text
py -3.11 -m unittest tests.test_review_search_audit tests.test_review_search_forward_cases -v
Ran 45 tests
OK
```

这 45 项已经包含 H01–H21、R2-01–R2-08 和 strict-mode 测试，不能与 R3 结果相加后宣传为一个统一的随机准确率。

## 人工金标准与严格通过条件

R3 在运行前先为每个案例写定完整 gold，包括：综述自指类型、披露模式、全部 `evidence` 字段、系统综述缺失元素、诊断 code 与 level，以及判断理由。严格通过要求所有这些字段逐项一致；任何会改变作者行动或 strict 门禁结果的字段不一致即判失败。

人工判断遵循以下原则：

1. 本文最终实际采用的文体高于被引用论文题名、先前计划或已放弃方案中的方法词；中文“系统评价”按常用学术语义视为 systematic review。
2. 系统/范围/荟萃综述必须有真实当前存在的数据库特异检索记录，以及文献对象的纳排、去重、筛选和流程记录。
3. 数据库字段或邻近算符必须属于检索语境；材料变量 `TS`、患者电子记录、仪器记录不能冒充检索式或文献选择记录。
4. supplement 的现在时存在、未来承诺和当前缺失必须分开；信息顺序变化不能改变语义。
5. 来源角色按语义判断，而不是只接受 `retrieve/verify` 等固定动词；作者资料库的来源、时期、进入规则和来源保留均可用自然变体表达。
6. 叙述综述可同时交代“不是系统综述”和“不作穷尽覆盖推断”；二者功能不同，不应仅因跨两个段落命中边界词而自动判为重复。

## 逐案结果

| ID | 对抗点 | Gold | 脚本实际输出 | 判定 |
|---|---|---|---|---|
| R3-01 | 中文 `系统评价` 同义自指，完整系统记录 | systematic；structurally complete | `unspecified`；`review_type_not_declared` | **失败**：类型漏识别；strict 门禁被绕过 |
| R3-02 | `No systematic review was undertaken` 被动否定 | narrative；transparent narrative scope | `unspecified`；`review_type_not_declared` | **失败**：否定式未建立叙述类型 |
| R3-03 | PsycINFO/EBSCO `TX` + `N3` | systematic；structurally complete | 与 gold 全字段一致 | **通过** |
| R3-04 | `Query concepts were:` 后接长分号库存 | inventory=true；伪检索式诊断 | inventory=false；无诊断 | **失败**：关键词库存标签覆盖过窄 |
| R3-05 | 同段材料变量 `TS = 25 °C` | executable=false；系统记录缺检索式 | executable=true；structurally complete | **失败**：领域字段串扰；strict 假通过 |
| R3-06 | 同段患者电子健康记录筛选与队列流程 | 文献 screening=false、flow=false | 两项均 true；structurally complete | **失败**：多主体语义未分离；strict 假通过 |
| R3-07 | 同段光谱仪 duplicate records | 文献 deduplication=false | deduplication=true；structurally complete | **失败**：非书目 records 串扰；strict 假通过 |
| R3-08 | `obtained PDFs` / `corroborate metadata` 来源角色同义表达 | publisher 与 DOI 角色均明确 | 两项均 false；报角色缺失 | **失败**：语义明确仍误报 |
| R3-09 | 作者全文库用 `inclusion` 名词表达进入规则 | collection boundary 已完整 | role=false；报 boundary 缺失 | **失败**：进入规则形态覆盖不足 |
| R3-10 | supplement `slated for deposit` 且当前未附 | planned/placeholder；系统记录不完整 | claimed present；structurally complete | **失败**：未来附件当作现存；strict 假通过 |
| R3-11 | `strings ... are provided in Supplementary Methods` 倒置信息顺序 | claimed present；structurally complete | supplement absent；systematic incomplete | **失败**：现存附件漏报；strict 假拒绝 |
| R3-12 | 文体边界和覆盖边界分属不同功能 | 两段 boundary，且无重复诊断 | 报 `repeated_non_systematic_disclaimer` | **失败**：段落计数替代功能判断 |
| R3-13 | `PubMedBERT`、`ScopusNet`、model versions | 无数据库、无版本处理泄漏 | 与 gold 全字段一致 | **通过** |
| R3-14 | 被引用论文题名含 `systematic review`，本文自指 narrative | narrative；partial scope | systematic；critical incomplete | **失败**：引文标题覆盖本文类型 |
| R3-15 | 已放弃 systematic 计划，最终明确 narrative | narrative；partial scope | systematic；critical incomplete | **失败**：先前计划覆盖最终实施类型；另漏 selection logic |
| R3-16 | PubMed `[Majr]` 与 `[Publication Type]` 字段 | executable=true；structurally complete | executable=false；systematic incomplete | **失败**：合法字段白名单漏项；strict 假拒绝 |

## 混淆与缺陷归纳

### P0：strict systematic 仍存在假通过

1. **类型漏识别可直接绕过 strict。** R3-01 的中文“系统评价”未进入 systematic 集合，因 `missing_systematic_elements` 只对已识别的系统类型计算，strict 会返回成功，而不是指出类型解析不确定。
2. **同段多科学主体没有关系约束。** R3-05 的材料变量 `TS` 被当作 WoS 字段；R3-06 的患者记录筛选和队列流程被当作文献筛选/流程；R3-07 的仪器记录被当作文献去重。三例均把实际不完整记录升级为 `systematic_record_structurally_complete`。
3. **未来 supplement 仍是开放式漏网。** R3-10 的 `slated for deposit` 不在未来语态表，后续 `Supplementary Search Strategy` 词面即被记为当前存在。

这些不是表面诊断差异，而是会把 strict 退出码从应有的非零变成零的安全性缺陷。

### P1：类型优先级和语境归属不稳

1. R3-14 表明“本文引用了题名含 systematic review 的既往文章”仍可能因段首 `This review` 落入自指窗口而覆盖后文明确的 narrative 声明。
2. R3-15 表明 `planned as a systematic review` 会覆盖同句后部的 `final article is a narrative review`。类型解析需要识别计划、否定、终止、最终实施和被引对象，而不只是“自指词距方法词多少字符”。
3. R3-02 的 `No systematic review was undertaken` 未按非系统叙述处理。当前否定词表覆盖了部分前置 `not/did not`，但没有统一解析否定主语、被动语态和最终文体。

### P1：检索式与 supplement 的召回、精度同时不足

1. R3-04 的 `Query concepts` 长库存未被识别，说明 inventory 标签仍依赖有限固定短语。
2. R3-05 说明全局字段标记精度不足；字段 token 必须和特定数据库的查询语境绑定。
3. R3-16 的 `[Majr]`、`[Publication Type]` 为合法 PubMed 字段却被漏报，说明有限白名单又导致召回不足。
4. R3-10 与 R3-11 分别是未来→当前和当前→缺失的相反错误。更稳妥的方案是先解析附件是否“当前随稿存在”，再判断其中是否声称含各库字符串与运行日期，而不是依靠前后固定词序。

### P1：来源角色仍依赖固定动词形态

R3-08 已明确“获得 PDF”和“核对作者、年份、撤稿状态”，R3-09 已明确资料库来源、时期、进入规则和来源保留，脚本仍报警。规则需要覆盖名词化、同义动词和跨分句语义；同时必须保持保守，不能因任意 `PDF`、`provenance` 或 `inclusion` 单词就自动判完整。

### P2：重复边界诊断缺少功能判断

R3-12 的两句分别回答“本文是什么文体”和“可否据此推断覆盖全面性”。当前 `coverage_boundary_paragraphs > 1` 即报重复，会把互补披露误作冗余。该诊断应比较命题功能和信息增量，或至少降为人工检查提示而非确定性修改建议。

## 总体评分解释

- 严格案例分数：**2/16 = 12.5%**。
- 当前回归分数：**45/45**，仅证明既有 H/R2 固定案例未回退。
- R3 中系统门禁方向性错误：5 个假接受路径（R3-01、05、06、07、10），2 个假拒绝路径（R3-11、16）。
- 叙述综述相关误差：类型漏识别或误升 systematic（R3-02、14、15）、伪检索式漏报（R3-04）、来源角色误报（R3-08、09）、重复边界误报（R3-12）。

本分数是有意选择困难边界后的对抗集表现，不是自然稿件分布上的准确率、召回率或质量分数。它适合暴露失败模式，不适合估计真实世界发生率。

## 外部有效性边界

即使未来 R3 全部通过，仍不能据此声称工具在真实综述上普遍可靠，原因包括：

1. 16 例是短文本、人工构造、单评估者定 gold，未覆盖长篇 DOCX 中表格、脚注、引文样式、跨节共指和混合语言排版。
2. 只抽样了少量数据库和字段。各平台语法、接口迁移、索引名称和厂商字段会变化；合法 token 也可能在材料学正文中承担非检索含义。
3. 结构词命中不能验证补充文件真实存在、检索式可在当前界面运行、筛选台账真实、去重算法执行正确或 PRISMA/目标期刊最新要求得到满足。
4. 叙述性与系统性综述之间还存在 rapid、umbrella、integrative、realist、mapping 等类型，本脚本当前本体没有完整覆盖。
5. 来源角色、否定、自指和时间状态具有开放式自然语言变体；继续扩充固定正则可能同时增加误报和漏报。

因此，最安全的产品边界仍是：输出只表示文本中检测到的结构信号，任何“可复现”“完整”“符合指南”或“投稿就绪”判断都必须由人工核对真实查询、附件、筛选记录和当前场所规范。

## 建议

1. 在任何进一步宣传或作为阻断门禁使用前，优先修复 R3-01、05、06、07、10 五条假接受路径。
2. 类型解析应先判定语义主体和状态：本文最终实施、既往文献、计划、否定、放弃、引用标题分别处理；不确定时宁可返回类型冲突/需人工确认，也不要静默跳过 strict。
3. 把查询字段、筛选、去重和流程信号绑定到文献检索主体；同一段不等于同一科学对象。
4. supplement 建议采用三步判定：当前是否存在、是否明确指向检索记录、是否声称含数据库特异字符串和运行日期。未来承诺不能满足系统门禁。
5. 修复后把 R3-01–R3-16 冻结为第三轮独立回归，再用新的未知 R4 评估；不要只在本轮措辞上追加正则后宣称泛化问题已解决。
