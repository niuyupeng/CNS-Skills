# 综述检索披露第六轮修复后复评（R6，2026-08-30）

## 结论

R6 的历史初测保留在 review-search-sixth-round-evaluation-2026-08-30.md：
12 条 gold 在脚本运行前冻结，首次真实 CLI 黑盒运行为
**3/12 全字段严格通过**、**201/240 原子字段一致**和
**7/12 strict 退出方向一致**，其中有 1 条 strict 假接受和 4 条
strict 假拒绝。本复评不删除、改写或用修复后数字取代该历史。

在不修改 R6 的案例文本、expected evidence、diagnostics 或 strict gold
的前提下，修复后的同一全字段比对为：

- **12/12 全字段严格通过**；
- **240/240 原子字段一致**；
- **12/12 strict 退出码一致**；
- 该冻结集上的 strict 假接受为 0，假拒绝为 0。

H、R2、R3、R4 和 R5 的 81 条既有数据驱动案例仍为 **81/81**；
加入 R6 后，六组案例合计 **93/93**。这些是已知、公开、确定性的回归集
结果，不是真实长篇稿件上的准确率、敏感度、特异度或开放域泛化保证。

## 复评方法

1. 从 review-search-sixth-round-cases.jsonl 读取 12 条冻结案例；复评前后
   均核对 12 行、12 个唯一 ID 和 gold SHA-256。
2. 每例比较 20 个原子字段：类型、披露模式、全部 evidence 字段、
   systematic 缺失项以及 diagnostic code/level；只有 20/20 才计整例通过。
3. 每例另以真实 CLI --strict-systematic 运行，将进程退出码与
   expected_strict_exit 单独比较。
4. tests/test_review_search_forward_cases.py 现在动态载入 R6，并在导入时
   锁定 12 个唯一 ID、R6-01—R6-12 连续序号及每条 0/3 strict gold。
   12 条数据驱动测试核对全字段，另有独立套件级测试黑盒核对全部
   12 条 CLI 退出码。

## 根据 R6 失败修正的规则

- **非书目字段碰撞：** 将 .tw. 等 Ovid 形状令牌绑定到检索语境；同句已
  明确定义为流变仪或 assay 字段，或明示“不是书目检索字段”时，不再升级
  为可执行查询。
- **选择动作的科学主体：** 排除组织切片、标本条码和病理学家等非书目
  流程；同时恢复 Reports were eligible、this bibliographic set was
  deduplicated 和 Search exports were deduplicated 等正对照。
- **文体归属：** 将 editor/reviewer comment 中的未加引号类型短语与本文
  自指分开；作者明确否定的外部评语不再覆盖最终 structured narrative 声明。
- **supplement 当前性：** 对 already included with this submission 且给出
  平台命令和执行日期的记录优先判为当前存在；被
  No ... is planned because ... already included 否定的未来存储不再覆盖
  现有附件。封锁、未随稿和未来发布仍保持 placeholder。
- **作者全文库边界：** 识别 author-maintained Zotero full-text library
  等自然同义表达，并在集合名称之后有限扩展形成时间、来源流、同一进入规则
  和条目级溯源的局部窗口。
- **次级来源角色：** publisher platform 和 DOI landing page 被合并为
  these resources 且只给出混合功能时，两者都保持未明确，不再对任一来源
  过早标为角色已披露。
- **自然叙述范围：** 增加 chosen、built from purposive examples、
  search vocabulary 与分号概念族等常见表达；将“语料覆盖边界”与
  “发生比例推断边界”作为两种功能，避免误报重复免责。

## 回归命令与结果

    py -3.9 -m unittest tests.test_review_search_audit tests.test_review_search_forward_cases
    Ran 118 tests
    OK

    py -3.11 -m unittest tests.test_review_search_audit tests.test_review_search_forward_cases
    Ran 118 tests
    OK

    py -3.9 -m unittest discover -s tests -p test_*.py
    Ran 191 tests
    OK

    py -3.11 -m unittest discover -s tests -p test_*.py
    Ran 191 tests
    OK

其中 test_review_search_audit 为 20 项；
test_review_search_forward_cases 为 98 项（93 条数据驱动案例加 5 项
套件级门禁）。两套 Python 的综述检索模块均为 118/118，完整仓库测试
均为 191/191。

## 文件快照

- R6 初测审计器（历史快照）：
  23C68A30147D1A475B56248CD5DE818DAC3FA5D2CDC32D1D2D1E8A2109FC19E2。
- 修复后 scripts/review_search_audit.py：
  61975D99BB5248400E6B146220D18FF8F4803D6045B649C4D7ACA299B525E11C。
- tests/test_review_search_audit.py：
  28A0C744A8C2F0ED64CBE01E701410CCA5C26D440BE80B589C52B774ED0BAA0E。
- tests/test_review_search_forward_cases.py：
  66FBD63CE91F26DE71E292E18021011D0D9880E63207A11913DEF0C1EE1233CB。
- 冻结 R6 gold evals/review-search-sixth-round-cases.jsonl：
  6C1E885A701BA2EC05798615A5864566ADE005055059BC356FE76667C3E44793。

## 有效性与产品边界

1. R6 修复后 12/12 只说明这 12 条已知短文本的公开 gold 已被回归锁定；
   它不证明未知措辞、真实长篇 DOCX 或其他学科的开放域泛化。
2. 对 critical、state-of-the-art、rapid、umbrella、integrative、realist、
   mapping、living 等未支持类型，strict 0 只表示当前类型门禁未适用，
   不表示方法完整。
3. 审计器不打开被引用的 supplement，不执行数据库查询，不验证导出、去重、
   筛选或流程账本的真实性，也不判定 PRISMA 或目标期刊的当前合规性。
4. systematic_record_structurally_complete 始终只是有限文本结构信号；
   零退出码不是接受、真实性、可复现性或投稿合规决定。真实检索材料与当前
   指南必须人工核对。

R6 是本次发布前最后一轮对抗集；本复评没有生成 R7。
