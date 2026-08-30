# 综述检索透明度规则独立前向评估（2026-08-30）

> **历史阶段报告。** 本文保留 H01—H21 首次评估及当轮修复结果，不代表当前完整套件；当前回归范围与边界见 [`evals/README.md`](README.md)。

## 结论

- 首次独立留出评估共 21 个案例，修复前严格通过 7 个（33.3%），失败 14 个；下表保留这次失败记录，避免抹去工具演进历史。
- H01–H21 已冻结在 `evals/review-search-forward-cases.jsonl`，由 `tests/test_review_search_forward_cases.py` 逐条执行；另有 2 项严格模式退出码测试。修复后为 **21/21 前向案例通过、23/23 前向测试通过**，与原 14 项基线合计 **37/37 通过**。案例只在数据驱动前向套件中执行一次，未通过重复测试函数放大公开测试数。
- 另对当前中文、英文主稿第 2.1 节作了只读判断，不计入 21 个留出案例。
- **修复后合入建议：可作为透明的结构分诊工具合入，但不能作为可复现性证明。** 当前保守输出使用 `systematic_record_structurally_complete`，并明确声明它不核实补充文件是否真实存在、不证明检索式可运行，也不替代人工核验和目标场所指南。

## 修复后复测

本轮针对首次评估暴露的问题完成了以下修复，并由 H01–H21 锁定：

1. 把未来时态或占位式 supplement 记为 `planned_or_placeholder`，不能满足系统综述的检索式要求；系统综述因此保持 `systematic_record_incomplete`，叙述综述则获得单独的占位附件提示。
2. 将文献去重限定为 records/citations/references/articles/search results 等书目对象；材料候选去重不再冒充文献去重。
3. 在检索相关段落的局部上下文中提取流程信号，降低正文中普通 `version`、`deduplication` 等词的串扰。
4. 加入系统/范围/荟萃类型声明的否定和自指约束，指南书名及他文标题不再自动改变本文文体。
5. 收紧“可执行式”信号；孤立 Boolean 词和关键词库存不算数据库特异查询，并补充 CINAHL、PsycINFO、BIOSIS、CNKI、万方和 SinoMed 等来源识别。
6. 补充中英文日期、补充材料、覆盖边界、出版社/DOI 页面角色及作者资料库边界表达。

通过命令：

```bash
python -m unittest tests.test_review_search_audit tests.test_review_search_forward_cases -v
```

结果：37 tests，全部通过，其中 21 项为独立前向案例、2 项为严格模式退出码测试。这里的“通过”只表示这些已声明结构信号与人工金标准一致，不表示任何具体系统综述已经被证明可复现。

## 评估边界与人工金标准

首次评估前已完整读取项目恢复档案、`cns-skills/SKILL.md`、两份指定 reference、脚本和当时的测试。首次评估只写入本报告；随后才根据失败项修改脚本并把案例冻结为独立前向回归集。两份主稿始终只读，未因该评估而改变。

人工金标准仅判断“检索与选择披露是否与文体相称”，不对综述科学质量打分：

1. 叙述性综述的透明范围说明应交代主要书目来源、截止日期、选择目的或逻辑，以及不作全面覆盖推断的边界；无需独立 Methods 标题或 PRISMA 流程。
2. 系统综述、范围综述和荟萃分析须有真实存在、可重跑的数据库特异检索记录，以及纳排、文献去重、筛选和流程记录。未来拟补的 supplement 不算现存记录。
3. 长关键词清单、孤立 Boolean 词或一般概念组合不等于数据库特异可执行检索式。
4. 出版社页面、DOI 页面和作者全文库可以使用，但必须说明发现、获取或核验角色；已经明确说明的角色不应再次报警。
5. Methods 标题本身不加分；没有该标题本身也不扣分。具体目标期刊或领域指南高于通用文体习惯。

严格“通过”要求综述类型、披露模式、关键 evidence 字段和诊断均与人工判断一致；只要一个会改变用户行动的重要字段错误，即判失败。

## 21 个独立留出案例（首次评估，修复前记录）

这些输入未出现在现有 `test_review_search_audit.py` 中。

| ID | 反例或边界 | 人工金标准 | 工具结果要点 | 判定 |
|---|---|---|---|---|
| H01 | 英文简洁叙述综述，用 `completeness is not claimed` 限定覆盖 | `transparent_narrative_scope` | 未识别该边界，报 `partial_narrative_scope` | 失败，漏报 |
| H02 | 无 Methods 标题、披露充分的英文叙述综述 | transparent；无诊断 | 与人工一致 | **通过** |
| H03 | 有 Methods 标题，逗号分隔的长关键词清单，无数据库/日期/边界 | partial，且应报伪检索式 | partial，但逗号清单未触发伪检索式 | 失败，漏报 |
| H04 | 分号清单后接 `biomaterial OR hydrogel AND machine learning`，无字段或数据库语法 | 应报伪检索式 | 两个 Boolean 词使 `exact=True`，未报警 | 失败，漏报 |
| H05 | 英文叙述综述，真实 Supplementary Search Strategy 已含各库可执行式与运行日期 | transparent；supplement=true；无诊断 | 与人工一致 | **通过** |
| H06 | 系统综述称 Supplementary Search Strategy “will be added before submission” | incomplete，缺实际检索式/现存补充记录 | 把未来承诺当现存 supplement，报 reproducible | 失败，漏报 |
| H07 | 无 Methods 标题，但 MEDLINE/Scopus 各有可执行式且系统流程完整 | reproducible systematic | 与人工一致 | **通过** |
| H08 | 有 METHODS 标题，但系统综述只有分号关键词清单 | incomplete，缺 executable query；critical | 与人工一致 | **通过** |
| H09 | 范围综述，PubMed/Embase 完整流程，真实 Supplementary Table S1 含各库策略 | reproducible scoping record | 与人工一致 | **通过** |
| H10 | 中文范围综述：`截至2026年7月`，`附录S1列出…完整检索式`，流程完整 | reproducible scoping record | 日期与附录措辞均漏识别，报 critical incomplete | 失败，误报 |
| H11 | 英文荟萃分析，WoS 与 Embase 各有数据库特异式且流程完整 | reproducible meta-analytic record | 与人工一致 | **通过** |
| H12 | `We did not conduct a systematic review` | 否定性非系统综述，不应触发系统门禁 | 误判 systematic 并发 critical | 失败，误报 |
| H13 | `本文并未开展系统综述` | 否定性非系统综述 | 误判 systematic 并发 critical | 失败，误报 |
| H14 | PubMed 为书目库，publisher 仅取全文，DOI 页仅核元数据，英文角色已明确 | transparent；不应报角色缺失 | 仍报 `discovery_and_verification_sources_need_roles` | 失败，误报 |
| H15 | 作者全文库的来源、时期、进入选择流程均已明确 | 不应报 collection boundary 缺失 | 仍报 `author_collection_boundary_needed` | 失败，误报 |
| H16 | 与 H14 等价的中文来源角色说明 | 不应报角色缺失 | 仍报角色缺失 | 失败，误报 |
| H17 | 仅用 CINAHL 的完整系统综述，含 CINAHL `MH` 语法 | named database + executable query；reproducible | CINAHL 和 `MH` 均漏识别，报 critical incomplete | 失败，误报 |
| H18 | 正文只提到 *Cochrane Handbook for Systematic Reviews*，文章自身是 invited critical overview | `unspecified`，指南书名不是类型声明 | 因指南标题误判 systematic | 失败，误报 |
| H19 | 目标期刊 invited Review 文体要求不设 Methods 标题，但范围披露充分 | transparent narrative | 与人工一致 | **通过** |
| H20 | 分号关键词清单；后文写 `NOT systematic AND coverage was not estimated` | 应报伪检索式 | 否定句中的 NOT/AND 使 `exact=True`，未报警 | 失败，漏报 |
| H21 | 系统综述未报告文献去重；应用章节只出现“generative-model candidate deduplication” | incomplete，缺 bibliographic deduplication | 材料候选去重冒充文献去重，报 reproducible | 失败，漏报 |

汇总：H02、H05、H07、H08、H09、H11、H19 通过；其余 14 个失败。

## 主要缺陷与建议

### P0：可能让严格系统综述门禁假通过

1. **补充材料只做词面存在判断。** H06 中 “will be added” 也被记为现存记录。建议把 supplement 分为 `verified_present`、`claimed_present`、`planned_or_placeholder`；只有实际随稿文件或明确现存记录可满足严格门禁。
2. **全文语境串扰。** `deduplication`、`versions`、`PRISMA` 等在全文任意位置命中；H21 的材料候选去重因此冒充文献记录去重。建议先定位 review-scope/search/methods 段落，再在局部窗口内提取证据，并输出证据段落或 span。文献去重还应要求 record/citation/article 等语义主体。

### P1：类型、检索式和双语识别不稳

1. **类型声明缺少否定和语境。** 扩展 `did not conduct/perform`、`并未开展/没有进行` 等否定式；要求 systematic/scoping/meta 词组与 `this review/we conducted` 等自指声明同处一段。指南、书名或他文标题不能自动变成本文类型。
2. **Boolean 判据过宽，关键词清单判据过窄。** `AND/OR/NOT` 只能在检索策略局部窗口内计数；仅有 Boolean 词不应等同 executable。数据库特异字段、邻近算符、受控词表和可重跑结构应与具体数据库绑定。库存检测需覆盖英文逗号、中文逗号/顿号及多行枚举。
3. **中英文日期与 supplement 表述覆盖不足。** 增加 `截至/截至…检索`、`附录S1列出检索式`、`补充表中提供完整策略` 等语序，同时排除将普通发表年份误当检索日期。
4. **数据库/平台表过窄。** 至少补 CINAHL、PsycINFO、BIOSIS、CNKI/中国知网、万方、SinoMed 等；更稳妥的是可扩展注册表加“被明确称为 database/index”的保守兜底，并保留 primary bibliographic / discovery / retrieval / verification 角色。

### P1：已充分披露仍报警

1. Publisher、DOI 页面和作者全文库目前一出现就报警。应在同句或邻句识别 `searched/discovered`、`retrieved full text`、`verified metadata/status`、`assembled from…between…` 等角色与边界；只有缺失字段才提示。
2. 覆盖边界需要支持 `completeness is not claimed`、`does not claim comprehensive coverage`、`不追求全面覆盖` 等常见表达。

### P2：输出命名与重复句诊断

`reproducible_systematic_record` 目前只表示少数结构词被命中，并不证明检索式真实可运行、补充文件存在或符合 PRISMA/目标期刊要求。修复前宜改为较窄的 `systematic_elements_detected`；最终可复现结论必须人工核对。`repeated_non_systematic_disclaimer` 也应比较句子功能和位置，而不是只按命中段落数判断。

该建议现已落实：H01–H21 已成为版本化数据驱动回归案例，并用严格模式退出码测试锁定 H06 和 H21 不得返回成功。

## 隐私安全的应用边界检查

首轮评估还用一段不随仓库分发的双语工作稿做过只读诊断。公开版不保留项目目录、文件名、题名或未发表文本，只保留由该检查抽象出的匿名反例 H21：材料候选去重、数据筛选或制备流程词不能冒充书目记录去重、文献筛选或 PRISMA 流程证据。H21 已进入版本化回归集；对任何真实稿件的判断仍不得从这份公开报告反推。

## 最终建议

首次评估提出的暂缓条件已经由 H01–H21 的 21/21 回归结果满足。当前实现可以合入为结构分诊工具，并继续保留以下边界：

1. `systematic_record_structurally_complete` 只表示当前文本中出现了规定的结构信号，不证明真实补充文件存在、检索式可执行或报告符合具体指南；
2. `--strict-systematic` 只能因缺失结构信号返回非零退出码，不能把零退出码解释为“系统综述已通过可复现性验证”；
3. 人工检查、真实附件、数据库特异检索式和当前目标期刊要求仍然具有最终权威；
4. 后续新增反例应继续进入版本化前向回归集，而不是扩张宣传口径。
