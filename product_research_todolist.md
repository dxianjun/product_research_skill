# Product Research TODO List

## 0. 执行规则（必须遵守）

1. 每完成一个功能块，先编写测试用例文档。
2. 对测试用例做合理性校验（主流程、异常流程、边界覆盖）。
3. 执行自动化测试。
4. 产出测试报告。
5. 仅在“该模块测试通过”后进入下一模块。

## 1. 模块执行清单

### 模块 01：竞品池管理（MVP）

- [x] 实现服务层（ASIN 导入、分层、标签、查询）
- [x] 编写自动化测试
- [x] 编写测试用例与合理性校验文档
- [x] 执行测试
- [x] 生成测试报告

关联文件：
- `src/competitor_pool.py`
- `tests/test_competitor_pool.py`
- `tests/module_01_test_cases.md`
- `tests/module_01_test_report.md`

### 模块 02：竞品变化检测（MVP）

- [x] 实现快照对比与字段变化识别
- [x] 编写自动化测试
- [x] 编写测试用例与合理性校验文档
- [x] 执行测试
- [x] 生成测试报告

关联文件：
- `src/change_detection.py`
- `tests/test_change_detection.py`
- `tests/module_02_test_cases.md`
- `tests/module_02_test_report.md`

### 模块 03：预警规则引擎（MVP）

- [x] 实现规则模型（阈值、波动率、连续天数、组合条件）
- [x] 实现告警分级（P1/P2/P3）
- [x] 实现去噪机制（合并、冷却）
- [x] 编写自动化测试
- [x] 编写测试用例与合理性校验文档
- [x] 执行测试
- [x] 生成测试报告

关联文件：
- `src/alert_engine.py`
- `tests/test_alert_engine.py`
- `tests/module_03_test_cases.md`
- `tests/module_03_test_report.md`

### 模块 04：告警通知中心（MVP）

- [x] 实现通知抽象层（站内/邮件）
- [x] 实现告警路由与订阅策略
- [x] 实现失败重试与幂等控制
- [x] 编写自动化测试
- [x] 编写测试用例与合理性校验文档
- [x] 执行测试
- [x] 生成测试报告

关联文件：
- `src/notification_center.py`
- `tests/test_notification_center.py`
- `tests/module_04_test_cases.md`
- `tests/module_04_test_report.md`

### 模块 05：日报/周报生成（MVP）

- [x] 实现报告模板（日报/周报）
- [x] 实现数据聚合与结论生成
- [x] 支持 Markdown 导出
- [x] 编写自动化测试
- [x] 编写测试用例与合理性校验文档
- [x] 执行测试
- [x] 生成测试报告

关联文件：
- `src/report_generator.py`
- `tests/test_report_generator.py`
- `tests/module_05_test_cases.md`
- `tests/module_05_test_report.md`

### 模块 06：竞品分析看板 API（MVP）

- [x] 实现竞品总览接口
- [x] 实现变化时间线接口
- [x] 实现我方 vs 竞品差距分析接口
- [x] 编写自动化测试
- [x] 编写测试用例与合理性校验文档
- [x] 执行测试
- [x] 生成测试报告

关联文件：
- `src/dashboard_api.py`
- `tests/test_dashboard_api.py`
- `tests/module_06_test_cases.md`
- `tests/module_06_test_report.md`

### 模块 07：市场监控（Should）

- [x] 实现关键词趋势聚合
- [x] 实现类目趋势监控
- [x] 实现新品/品牌动态跟踪
- [x] 编写自动化测试
- [x] 编写测试用例与合理性校验文档
- [x] 执行测试
- [x] 生成测试报告

关联文件：
- `src/market_monitor.py`
- `tests/test_market_monitor.py`
- `tests/module_07_test_cases.md`
- `tests/module_07_test_report.md`

### 模块 08：舆情监测（Should）

- [x] 实现评论主题聚类（规则版）
- [x] 实现情感趋势统计
- [x] 实现风险事件识别（差评激增、星级骤降）
- [x] 编写自动化测试
- [x] 编写测试用例与合理性校验文档
- [x] 执行测试
- [x] 生成测试报告

关联文件：
- `src/sentiment_monitor.py`
- `tests/test_sentiment_monitor.py`
- `tests/module_08_test_cases.md`
- `tests/module_08_test_report.md`

## 2. 全局保障任务

- [x] 建立统一测试入口与脚本（本地/CI）
- [x] 补充 `src` 模块初始化与包结构规范
- [x] 增加基础质量门禁（`compileall` + 单测）
- [x] 增加 ruff/mypy 静态检查
- [x] 建立测试报告索引文档
- [x] 输出上线前验收清单（功能、数据、告警、报告）

## 3. 当前状态

- 当前完成模块：`08 / 08`
- 当前可执行下一步：`全局保障任务与上线验收准备`
