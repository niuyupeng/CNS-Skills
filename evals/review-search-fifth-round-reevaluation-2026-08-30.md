# 综述检索披露第五轮修复后复评（R5，2026-08-30）

## 结论

R5 的原始失败记录保留在
`review-search-fifth-round-evaluation-2026-08-30.md`：冻结 gold 首次黑盒运行为
**5/20 全字段严格通过**、**350/400 原子字段一致**和
**13/20 strict 退出方向一致**，其中有 4 条 strict 假接受和 3 条
strict 假拒绝。本复评不删除、改写或用修复后数字取代该历史。

在不修改 20 条冻结 gold 的前提下，修复后的同一全字段比对为：

- **20/20 全字段严格通过**；
- **400/400 原子字段一致**；
- **20/20 strict 退出码一致**；
- 该冻结集上的 strict 假接受由 4 条降为 0，假拒绝由 3 条降为 0。

H、R2、R3 和 R4 的 61 条既有数据驱动案例仍为 61/61；加入 R5
后，五组案例合计 81/81。这些数字是固定回归集结果，不是自然稿件上的
准确率、敏感度或特异度。

## 复评方法

1. 读取 `review-search-fifth-round-cases.jsonl` 的 20 条冻结案例；案例文本、
   expected evidence、diagnostics 和 strict 退出码均未修改。
2. 对每条比较 20 个原子字段：类型、披露模式、完整 evidence、缺失项以及
   diagnostic code/level。只有 20 个字段全部相等才计为整例通过。
3. 每条另以 CLI `--strict-systematic` 运行，将实际进程退出码与
   `expected_strict_exit` 比较。
4. `tests/test_review_search_forward_cases.py` 现在动态载入 R5，并固定
   20 个唯一 ID、R5-01—R5-20 连续序号及每条 0/3 strict gold。
   数据驱动测试核对全字段，独立套件级测试黑盒核对全部 20 条 CLI 退出码。

## 根据 R5 失败修正的规则

- **科学主体绑定：** 将临床病例、电子病历、材料候选库与题录记录分开；
  只有明确书目先行词支持跨句去重、筛选和 flow 信号。
- **文体归属：** 阻止表题、指南名和已撤回/未实施的历史方案覆盖本文
  当前自指；未支持的 realist、living 和 mapping review 仍保守返回
  `unspecified`。
- **字段形状碰撞：** 当 `MH` 或 `TITLE-ABS-KEY` 在非书目数据库中被明确
  定义为材料/临床字段时，不将其作为文献检索式。
- **中文 supplement 三态：** 区分随稿存在、尚待上传和当前明确缺失；
  future/missing 不能满足当前检索记录要求。
- **来源角色指代：** 对跨一个记录句的 `Those platforms/pages`、
  “前述平台/上述页面”等明确名词回指恢复角色识别；当中间出现竞争先行词且
  只用 `They` 时保持人工核对提示。
- **中文叙述范围：** 恢复“未声称穷尽”等覆盖边界、自然案例选择语句和
  分号概念库存的识别，但不将概念库存升级为可执行查询。

## 回归命令与结果

```text
py -3.9 -m unittest tests.test_review_search_audit tests.test_review_search_forward_cases
Ran 105 tests
OK

py -3.11 -m unittest tests.test_review_search_audit tests.test_review_search_forward_cases
Ran 105 tests
OK
```

其中 `test_review_search_audit` 为 20 项，`test_review_search_forward_cases` 为
85 项（81 条数据驱动案例加 4 项套件级门禁）。Python 3.9 和 3.11 均为
105/105。

## 文件快照

- 首次评测审计器（历史快照）：
  `6A87BAC7E25DAEC8B465D9251C5A5B4BADB726A222AEFEB633F6AB533BD4EDAF`。
- 修复后 `scripts/review_search_audit.py`：
  `23C68A30147D1A475B56248CD5DE818DAC3FA5D2CDC32D1D2D1E8A2109FC19E2`。
- `tests/test_review_search_audit.py`：
  `28A0C744A8C2F0ED64CBE01E701410CCA5C26D440BE80B589C52B774ED0BAA0E`。
- `tests/test_review_search_forward_cases.py`：
  `850B9DDBC16CA2D765E8DA84053683C9CB119BCA6DBA471AA8633259B5FE45B3`。
- 冻结 R5 gold `evals/review-search-fifth-round-cases.jsonl`：
  `3EAA6DDB547F95AA417AB0E0C42E9D7B4180AFCA81E16262D10E8AD372FB861E`。

## 有效性边界

R5 修复后 20/20 只说明已知表达已被回归锁定。它不证明真实长篇综述上的
开放域泛化，也不证明引用的补充文件存在、检索式可运行、导出/去重/筛选日志
真实，或符合当前 PRISMA 和目标期刊规则。对未支持综述类型返回 strict 0，
表示门禁未适用，不表示方法完整或获得接受。真实检索材料和当前报告规范始终
必须人工核对。

本 R5 修复任务本身没有生成 R6；其后另一次独立任务冻结并运行了 R6。R6 的首次 3/12 失败快照与修复后 12/12 复评分别保存在 `review-search-sixth-round-evaluation-2026-08-30.md` 和 `review-search-sixth-round-reevaluation-2026-08-30.md`。
