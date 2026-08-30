# 综述检索披露第四轮新鲜对抗评测（R4，2026-08-30）

> **历史阶段报告。** 本文保留 R4 新鲜输入、当轮修复及随后 6 条发布红队探针的结果；当前完整状态见 [`evals/README.md`](README.md) 和后续 R5 报告。

## 结论

- R4-01—R4-16 在实现加固前严格逐字段匹配 **5/16**；通过项为 R4-01、R4-02、R4-06、R4-08 和 R4-16。
- 16 条 gold 在修复前已写定。另一名独立审查者随后逐条复核，结论为 **16/16 可接受、必须修改 0 条**。
- 修复后 R4 为 **16/16**，H、R2、R3 无回退。一次独立的修复后代码审查又构造出 6 条同义边界探针，最初均复现发布阻塞错误；修复并逐条锁定后，综述检索两模块为 **84/84**，完整测试套件为 **157/157**。
- 这些数字是公开、确定性的对抗回归结果，不是自然稿件分布上的准确率、召回率或质量分数。

## 新鲜集暴露的问题

初次运行失败 11 条，覆盖了此前案例未锁定的边界：

1. 已撤回大纲中的 scoping 标签覆盖最终 integrative 文体；
2. 未加引号的外部论文题名和指南名称被误作本文 systematic 自指；
3. 明确否定 narrative 后实施 systematic 的顺序解析错误；
4. 细胞实验中的 `TX` 数据字段被误作数据库查询字段；
5. 患者电子病历的跨段指代被误作书目去重、筛选和流程；
6. 已附 supplement、未来 deposit 和明确未随稿三种状态相互混淆；
7. publisher/DOI 页面的跨句角色和作者全文库的跨段边界未被识别。

修复按语义主体、状态和邻接指代收紧规则，没有放宽 gold。R4-09、R4-10、R4-12、R4-13 已锁定为 strict 拒绝；R4-07、R4-08、R4-11 已锁定为 strict 接受。测试还单独断言：零退出码不是录用、真实性、可复现性或报告规范符合性结论。

## 修复后发布红队

R4 全绿后，另一名只读代码审查者没有查看实现者的预期关键词清单，而是从同类科学语境重新改写输入。它暴露出 6 条仍会改变 strict 方向的路径，随后各自成为独立测试：

1. 光谱仪的 platform commands 与 execution dates 冒充检索附件；
2. “supplementary files did not include the search strategy” 被否定词面反向识别为当前附件；
3. “Cells were cultured with N3 fibroblasts” 中的培养语境冒充邻近检索算子；
4. `Lee et al. reported This Systematic Review ...` 的未加引号外部题名覆盖本文 narrative 自指；
5. 结果随访至 2025 年被误作检索截止日期；
6. 患者电子病历在相邻段落中的隐式承接再次冒充书目去重、筛选与流程。

六项在修复前均可复现错误字段或 strict 方向，修复后 **6/6** 通过。这里把 R4 称为“新鲜输入后的对抗回归”，而不是继续把修复后已见数据宣传为未知 holdout。

## 冻结范围

- `scripts/review_search_audit.py`：903 行，SHA-256 `70EAF378E1DF0735E628AF49770EA8E90E6DB6E7EBB51FC22E0E8C1E75D3E0AA`
- `tests/test_review_search_audit.py`：273 行，SHA-256 `28A0C744A8C2F0ED64CBE01E701410CCA5C26D440BE80B589C52B774ED0BAA0E`
- `tests/test_review_search_forward_cases.py`：188 行，SHA-256 `13492C813307CA8ABB5C2C8C4C1881CC3D84054EED9126BB84D179A03136C495`
- `evals/review-search-fourth-round-cases.jsonl`：16 行，SHA-256 `19D1EF8AEDDF28D96B4AF32A131314299F5A797CB24EBE93A0A59E12CD7BE8F4`

R4 具有 16 条唯一、连续的 ID，并与 H/R2/R3 做跨轮唯一性检查。每个案例逐项比较类型、披露模式、全部证据字段、系统综述缺失元素以及诊断 code/level；不能只比较最终退出码。

## 保留边界

1. 类型本体仍是闭集。rapid、umbrella、integrative、realist 等未支持类型返回 `unspecified`，必须人工分类；它们不能因为未进入 strict 门禁就被视为通过。
2. 当前三态把未来计划和明确缺失都归入 `planned_or_placeholder`。这足以阻止假通过，但未来可拆为 `future_planned` 与 `explicitly_missing`。
3. 工具不打开引用的 supplement、不执行数据库查询、不检查搜索导出，也不验证去重或筛选日志；它只报告文本结构信号。
4. 16 条短文本对抗样本不能覆盖真实长篇 DOCX 的所有表格、脚注、引文标题、跨节共指、数据库语法和混合语言表达。

因此，R4 的意义是证明这些已知高风险边界已被公开锁定，而不是证明规则已经穷尽自然语言或真实综述流程。
