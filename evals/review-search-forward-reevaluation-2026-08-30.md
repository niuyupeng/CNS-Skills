# 综述检索透明度规则独立复评（2026-08-30）

> **历史快照，现已被后续修复取代。** 本报告保留第二轮反例首次运行时的失败记录，不代表当前实现。R2-01—R2-08 已全部固化为公开回归案例并通过；当前完整回归结果为 **178/178**。`systematic_record_structurally_complete` 仍只表示文本结构信号齐全，不验证检索真实性或可复现性。

## 结论

- 锁定前向集 H01–H21：**21/21** 逐字段符合 JSONL 金标准。
- `tests/test_review_search_forward_cases.py`：**23/23** 通过，其中 21 项为动态案例，2 项为 strict-mode 接受/拒绝测试。
- 当前两个综述检索测试模块：**105/105** 自动化测试通过；整个 `tests/` 目录为 **178/178**。上述 23 项已包含在相应总数中，不能重复相加。
- 独立第二轮、未预告的新反例：**0/8** 严格符合人工金标准；8 个均暴露剩余泛化缺陷。
- **不建议把当前实现合入为可靠的 strict systematic 门禁。** 第一轮缺陷已得到针对性修复，但第二轮仍发现 3 条可使不完整系统综述假通过或绕过系统门禁的路径。若仅作为带明确免责声明的非阻断式 triage，可继续开发；若合入意味着可依赖退出码或 `systematic_record_structurally_complete`，应暂缓。

## 复评快照与写入边界

最终复评基于以下稳定快照：

- `scripts/review_search_audit.py`：566 行，SHA-256 `E0BA29B0907FB95B4A246FE59B6055C461CE76547626E138117C8F87C66327C2`
- `tests/test_review_search_audit.py`：172 行，SHA-256 `01896C9265EAAE5DFBF9BA73A70019A98C3C90227B4A2184ABDDA5E8F8877B75`
- `tests/test_review_search_forward_cases.py`：96 行，SHA-256 `78C97FA5AEA276D7689391AF3F40192D575048068506D130BDD2361FF2CB6332`
- `evals/review-search-forward-cases.jsonl`：21 行，SHA-256 `96C55DF251D2F00C4D3605215883DB9505C9562F88EB7BFC931AB16C56EB146B`

本轮没有修改脚本、tests、README、JSONL 或其他核心文件。唯一有意写入路径为本报告。

## 1. H01–H21 逐条复核

动态测试对每个 JSONL 记录逐项比较：

1. `expected_declared_type`；
2. `expected_disclosure_pattern`；
3. `expected_evidence` 的全部顶层字段；
4. `selection` 内的 eligibility、selection logic、deduplication、screening、flow accounting 和 version handling；
5. diagnostic code 的内容与顺序。

结果为 21/21，无字段或诊断分歧。另两项 strict-mode 测试确认：

- H06（未来拟补检索策略）与 H21（材料候选去重冒充文献去重）均返回退出码 3；
- H07（结构完整且无 Methods 标题）返回退出码 0。

这证明第一轮发现的固定措辞已被有效锁定，但不证明规则已经覆盖新的语序、语境和数据库语法。

## 2. 第二轮独立反例

第二轮案例在运行前未向实现者披露，也未写入 tests 或 JSONL。人工金标准继续遵循“类型自指声明优先、检索证据须属于文献检索、角色披露按语义而非固定语序、真实数据库语法不应被有限白名单误杀”的原则。

| ID | 新输入要点 | 人工金标准 | 当前输出 | 判定 |
|---|---|---|---|---|
| R2-01 | 系统综述段落缺文献去重、文献筛选和文献流程；相邻段落仅写影像数据 `duplicate records`、两人筛显微图像及制备 `flow diagram` | systematic + incomplete；三项均缺失 | 三个相邻领域术语均被当作文献检索证据，报 structurally complete | 失败，strict 假通过 |
| R2-02 | 正文明示 `We conducted a systematic review` 且结构完整；末句只说 prior narrative reviews 用于术语背景 | systematic + structurally complete | 全文任意 `narrative reviews` 优先，误判 narrative + partial | 失败，类型门禁绕过 |
| R2-03 | 中文 `本研究并非系统综述`，随后说明为代表性案例更新 | narrative + partial | `并非` 未进入否定窗口，误判 systematic + critical incomplete | 失败，误报 |
| R2-04 | `Full-text retrieval was performed through publisher platforms`；`metadata ... were checked against DOI landing pages` | 两个来源角色均已明确；无诊断 | 因角色词位于来源名之前而未识别，报角色缺失 | 失败，误报 |
| R2-05 | 数据库提醒、机构库和 2018–2026 时间范围置于 author-curated collection 之前；下一句明确所有记录走同一 eligibility 流程 | collection boundary 已完整；无诊断 | 只识别 collection 名称之后同句的固定线索，报 boundary 缺失 | 失败，误报 |
| R2-06 | Ovid MEDLINE 真实 `.mp.` 检索式：`hydrogel*.mp. AND biomaterial*.mp.`，其余系统结构完整 | executable query=true；structurally complete | `.mp.` 不在语法表，报缺 executable query | 失败，误报 |
| R2-07 | PubMed 真实 `[MeSH Terms]` 检索式，其他系统结构完整 | executable query=true；structurally complete | 仅识别 `[MeSH]` 等有限标签，漏掉 `[MeSH Terms]` | 失败，误报 |
| R2-08 | Supplementary Search Appendix 明示 `under preparation and will report`，系统综述无当前可执行式 | planned/placeholder；systematic incomplete | `report` 不在未来动作词表，误作 claimed present，报 structurally complete | 失败，strict 假通过 |

第二轮输入的关键原文如下，便于后续复现：

### R2-01：局部窗口领域串扰

> We conducted a systematic review. PubMed was searched through 30 August 2026 using hydrogel[Title/Abstract] AND biomaterial[Title/Abstract]. Inclusion and exclusion criteria were predefined.
>
> For the imaging dataset, duplicate records were removed, two reviewers independently screened microscopy images, and a flow diagram summarizes the fabrication pipeline.

### R2-02：既往叙述综述覆盖本文类型

> We conducted a systematic review. PubMed was searched through 30 August 2026 using hydrogel[Title/Abstract] AND biomaterial[Title/Abstract]. Inclusion and exclusion criteria were predefined. Duplicate bibliographic records were removed. Two reviewers independently screened titles, abstracts, and full texts. A PRISMA flow diagram reports records identified, screened, and excluded. Prior narrative reviews were used only to frame terminology.

### R2-03：中文否定变体

> 本研究并非系统综述，而是使用代表性案例的聚焦更新，不据此估计文献覆盖率。

### R2-04：来源角色的倒装/被动表达

> This narrative review searched PubMed through 31 July 2026. We selected representative experiments rather than an exhaustive census. Full-text retrieval was performed through publisher platforms; metadata and publication status were checked against DOI landing pages.

### R2-05：作者全文库的前置边界

> This narrative review searched Scopus through August 2026. We selected illustrative studies rather than an exhaustive census. Monthly database alerts and institutional repositories from 2018 to 2026 formed an author-curated full-text collection. Records from it underwent the same eligibility process.

### R2-06：Ovid `.mp.` 语法

> We conducted a systematic review. MEDLINE was searched through 30 August 2026 using hydrogel*.mp. AND biomaterial*.mp. Eligibility criteria were predefined. Duplicate bibliographic records were removed. Two reviewers independently screened titles, abstracts, and full texts. The PRISMA flow diagram reports records identified, screened, and excluded.

### R2-07：PubMed `[MeSH Terms]` 语法

> We conducted a systematic review. PubMed was searched through 30 August 2026 using "Biocompatible Materials"[MeSH Terms] AND "Hydrogels"[MeSH Terms]. Eligibility criteria were predefined. Duplicate records were removed. Two reviewers independently screened titles, abstracts, and full texts. The PRISMA flow diagram reports records identified, screened, and excluded.

### R2-08：未覆盖的未来 supplement 动词

> We conducted a systematic review. Embase was searched through 30 August 2026. Eligibility criteria were predefined. Duplicate records were removed. Two reviewers independently screened titles, abstracts, and full texts. The PRISMA flow diagram reports records identified, screened, and excluded. The Supplementary Search Appendix is under preparation and will report the full database strings.

## 3. 全套测试

最终运行：

```text
py -3.11 -m unittest discover -s cns-skills/tests -p test_*.py
Ran 105 tests
OK
```

命令输出中的 overwrite 错误文本来自专门验证“禁止覆盖输入文件”的负向测试，测试状态均为 `ok`，不属于失败。

## 4. 剩余限制与修复优先级

### P0：strict mode 仍可假通过

1. **局部窗口仍只按距离，不按科学主体。** 邻段的影像筛选、训练数据重复记录和制备流程图可满足 bibliographic screening、deduplication 和 flow accounting。应要求证据与 records/citations/articles 以及 literature search/screening 的主体关系成立；通用 `flow diagram` 不应单独满足流程记录。
2. **类型优先级可绕过门禁。** 全文出现任意 `narrative review(s)` 会先于本文自指的 systematic 声明返回 narrative。应先解析本文自指声明，再处理既往综述或指南名称；复数、引文标题和 `prior/previous` 上下文应排除。
3. **未来 supplement 动词表仍不封闭。** `will report`、`will make available`、`under preparation`、`forthcoming` 等都应使状态保持 planned。更稳妥的是只把明确的当前存在式标为 claimed present，而不是枚举所有未来动词。

### P1：常见语言和数据库语法仍有误报

1. 否定词需覆盖 `并非`、`并不是`、`No systematic review was conducted` 等，并避免被自指锚点吞掉。
2. 来源角色应允许角色说明位于来源名之前、被动语态和跨句共指；author collection 的来源、时段和 eligibility 也可能前置或跨句。
3. 数据库语法表至少需覆盖 PubMed `[MeSH Terms]`、`[Title]` 等标准字段及 Ovid `.mp.`、`.tw.`、`adjN` 等常见语法。长期看应按数据库建立小型语法注册表，并保持“结构信号”而非真实性证明的免责声明。

### 固有边界

即使所有正则命中，工具仍不能验证补充文件是否真正随稿存在、查询能否在当前数据库界面执行、筛选记录是否真实或目标期刊政策是否满足。因此 `systematic_record_structurally_complete` 只能表示文本结构信号齐全，不应等同可复现或投稿就绪。

## 5. 合入建议

当前重构相较首轮有实质进步：锁定 21 个缺陷已全部修复，105 项现有测试全部通过，Methods 标题与综述类型的基本边界也保持正确。但第二轮 8 个新例全部失配，且 R2-01、R2-02、R2-08 会影响 strict-mode 的安全性。

因此建议：

1. **暂不合入为阻断式门禁或发布为可依赖的 strict 检查。**
2. 可保留文字规则和非阻断式诊断定位，但用户界面应继续突出“structural signals only”。
3. 修复三个 P0 后，将 R2-01–R2-08 固化为第二轮回归集，再由新的未知案例复评。
4. 至少要求 strict mode 对 R2-01、R2-08 返回 3，并确保 R2-02 仍按 systematic 执行门禁，方可重新考虑合入。

## 本轮实际写入路径

- `cns-skills/evals/review-search-forward-reevaluation-2026-08-30.md`

除此之外，本轮未有意写入或修改任何项目文件。
