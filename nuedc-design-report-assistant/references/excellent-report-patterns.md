# Excellent NUEDC Report Patterns

Use this reference when drafting, rewriting, compressing, or reviewing a design report. It complements the full workflow: the report is the final evidence container, not a separate writing exercise.

Do not copy public winning reports. Learn structure, evidence discipline, and engineering expression only. 禁止复制优秀作品正文、图表、测试数据或 distinctive phrasing into user deliverables.

## Excellent Report Standard

An 优秀报告 makes the engineering chain visible:

`指标-设计-计算-测试-结论`

The reader should be able to trace every major claim from the problem requirement to a design decision, then to calculation or debugging evidence, then to measured data.

## Report Skeleton

Use this order unless the problem statement requires otherwise:

1. 摘要 and keywords.
2. 任务与指标分析.
3. 系统方案 and 方案论证.
4. 系统总体设计.
5. 理论分析与关键参数计算.
6. 硬件电路设计.
7. 软件/算法设计.
8. 系统调试与校准.
9. 测试方案与测试结果.
10. 指标完成情况 and error analysis.
11. 总结, limitations, improvements.
12. References and appendix when allowed.

For strict 8-page reports, combine sections but keep the evidence chain. Cut generic background before cutting measurements, formulas, or scoring alignment.

## Abstract Pattern

The abstract should be 200-300 Chinese characters when common NUEDC rules apply. It should include:

- Task object.
- Final scheme.
- Core hardware/software method.
- Key measured results if real data exists.
- Pending-test wording if data is not measured.

Avoid claims such as "all indicators are excellent" unless a measured table supports them.

## Requirement And Fulfillment Tables

Put a short requirement matrix early and a fulfillment matrix near the test section or conclusion.

Requirement matrix:

| ID | Requirement | Metric | Test condition | Priority | Design response |
|---|---|---|---|---|---|
| B1 | 待填写 | 待填写 | 待填写 | P0 | 待填写 |

Metric fulfillment matrix:

| Requirement | Design implementation | Test item | Test result | Error/score | Pass |
|---|---|---|---|---|---|
| 待填写 | 待填写 | 待填写 | 待实测 | 待计算 | 待判断 |

If real measurements are missing, keep the table but mark values as `待实测`. Do not convert pending rows into success claims.

## 方案论证 Pattern

A strong scheme comparison has rejection reasons, not only advantages.

| Dimension | Scheme A | Scheme B | Scheme C |
|---|---|---|---|
| Metric potential |  |  |  |
| Stability |  |  |  |
| Debug speed |  |  |  |
| Component availability |  |  |  |
| Test reproducibility |  |  |  |
| Main risk |  |  |  |

Good final choice:

`选择方案B，因为它在[核心指标]、[调试周期]和[测试可复现性]之间平衡最好；方案A虽然简单，但[具体指标]余量不足；方案C性能较高，但[器件/算法/机械]风险过大。`

## Module Design Cards

Turn hardware and software detail into module design cards before prose. In Chinese outputs, label this table as 模块设计卡.

| Module | Requirement served | Input | Output | Key parameter | Risk | Debug evidence |
|---|---|---|---|---|---|---|
| 待填写 | B1/F1 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 |

Then write each subsection in this order:

1. Purpose tied to a requirement.
2. Circuit or software mechanism.
3. Parameter choice and calculation.
4. Debug point and expected signal/log.
5. Risk and mitigation.

## Theory Calculation Pattern

Each calculation paragraph should follow:

`需求 -> 公式 -> 代入 -> 结果 -> 决策 -> 测试`

Example structure:

`为满足[指标]，需要保证[变量]不超过[阈值]。根据[公式]，代入[参数]得到[结果]。因此选择[器件/参数]，并在测试中通过[仪器/步骤]验证。`

Do not list formulas that do not affect a design decision.

## Hardware Writing Pattern

For each key circuit:

- Explain input/output range and electrical role.
- Give key parts and why they were selected.
- Include protection and reliability notes.
- State expected waveform or voltage at test points.
- Include calibration method if accuracy matters.

Useful subsections:

1. 主控与外设接口.
2. 信号调理/采样.
3. 驱动/执行.
4. 电源管理与保护.
5. 人机交互 and debug interface.

## Software Writing Pattern

Report software by structure and timing, not by code dump.

Required content:

- Main loop or state machine.
- Peripheral initialization table.
- Sampling/filter/control pipeline.
- Timing period and interrupt source.
- Fault handling.
- Debug output variables.

Software table:

| Function | Trigger/period | Input | Output | Key parameter | Debug method |
|---|---|---|---|---|---|
| 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 串口/示波器/日志 |

## System Debug And Calibration

Excellent reports mention real debugging and calibration, but keep it concise.

| Problem | Cause analysis | Fix | Verification |
|---|---|---|---|
| 待填写 | 待填写 | 待填写 | 待填写 |

For measurement projects, include calibration equations or before/after error tables. For motion/control projects, include repeated-trial stability data.

## Test Evidence Matrix

Use a 测试证据矩阵 before detailed data tables:

| Requirement | Instrument | Setup | Procedure | Data table | Pass/fail rule |
|---|---|---|---|---|---|
| 待填写 | 待填写 | 待填写 | 待填写 | 表X | 待填写 |

Detailed tables should include:

- Input or test condition.
- Theory/target value.
- Measured value.
- Absolute or relative error.
- Pass/fail.
- Notes for abnormal runs.

## Error Analysis

Do not write "误差来自元器件误差" only. Tie errors to the system:

| Error source | Mechanism | Estimated influence | Mitigation |
|---|---|---|---|
| Reference voltage | ADC scale changes | 待计算/待估计 | calibration/reference |
| Sampling noise | random fluctuation | 待填写 | filtering/grounding |
| Mechanical tolerance | position offset | 待填写 | alignment/repeated trials |

## Language Rules

Prefer:

- "在 5 V 供电、10 Ω 负载条件下重复测试 3 次，最大相对误差为..."
- "该截止频率用于抑制高频噪声，同时保持控制响应速度。"
- "由于暂无实测数据，本表保留待实测项，不能据此判断达标。"

Avoid:

- "方案简单可靠。"
- "测试效果很好。"
- "基本全部实现。"
- "具有较高创新性。"

## Compression Rules

When page budget is tight:

Keep:

- Requirement matrix.
- Scheme comparison and final reason.
- System block diagram.
- Key formulas linked to decisions.
- Module cards for high-risk modules.
- Test instruments, conditions, measured tables, error analysis.
- Fulfillment matrix.

Cut:

- Generic contest background.
- Long chip introductions copied from datasheets.
- Full source code.
- Decorative prose.
- Repeated descriptions of simple modules.

## Final Report Audit

Before claiming a report is strong, check:

1. Every requirement appears in a matrix.
2. Every major module maps to a requirement.
3. Every formula changes a design choice.
4. Every success claim has real measured data.
5. Every pending value is explicitly marked.
6. Anonymous information is absent.
7. The report can be compressed to the current page limit.
