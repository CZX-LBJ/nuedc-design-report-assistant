# Compliance And Quality

## Use Boundary

This skill is for赛前训练、课程设计、校赛训练、赛后复盘, and teacher/lab review. For an active official contest, the user must follow the current official rules and local赛区细则. Do not market or use the skill as a队外外援、代做、代写, or replacement for independent team work.

If the user asks for help during a formal live contest, keep assistance to rule reminders, safety, self-check checklists, and general study guidance unless the rules explicitly permit the requested help.

When a user asks for "省级一等奖", "国奖", or "获奖级别", treat it as a quality target for training and review. Do not promise any award. Say that awards depend on official scoring, physical implementation, team execution, real measurements, and competition conditions.

## Public-Source Learning Boundary

It is acceptable to learn from public official notices, problem statements, training resources, and公开优秀作品 at the level of structure and engineering method:

- How requirements are decomposed.
- How schemes are compared.
- How theory calculations support design choices.
- How hardware/software modules are described.
- How tests, errors, and fulfillment tables are presented.

Do not copy winning-report prose, circuit diagrams, original figures, exact measured data, or distinctive formatting into generated outputs. If a public source is used for current rules or factual claims, cite the URL in user-facing material when appropriate.

## Public Rule Signals To Preserve

The 2025 official process materials emphasize an engineering closed loop: design report, physical work, registration/materials, test records, and review/testing. Some赛区 materials specify anonymous reports, page limits, and a short Chinese abstract. These details can change by year and赛区, so tell the user to verify current rules before final submission.

Useful sources:
- 全国大学生电子设计竞赛培训网, 2025年全国大学生电子设计竞赛实施过程说明: https://www.nuedc-training.com.cn/index/news/details/new_id/333
- 上海赛区 2025 TI杯实施过程说明: https://nuedc-sh.sjtu.edu.cn/post_detail.php?id=42
- 全国大学生电子设计竞赛培训网资料列表: https://www.nuedc-training.com.cn/index/download/download_list/type/2
- 获奖作品选编示例: https://www.nuedcchina.com/upload/201905/bb1945dac213c3344eb72399e1ae9767.pdf

## Evidence Rules

| Evidence type | How to label | Forbidden wording |
|---|---|---|
| 理论计算 | “理论上/根据公式计算” | “实测达到” |
| 仿真结果 | “仿真显示/仿真条件为” | “现场测试证明” |
| 实物实测 | “实测值/测试仪器/测试条件/测试次数” | Unsupported “全部符合” |
| 待测项目 | “待实测填写/待现场复测” | Numeric-looking invented values |

Treat test data as three states:

- **Measured**: a table includes theory/measured/error values and test conditions.
- **Pending**: the report includes a待填写/待实测 table; this is acceptable for planning but cannot support a success claim.
- **Missing**: no theory/measured/error table exists; this is a high-risk report gap.

## Final QA Rubric

| Dimension | Excellent standard |
|---|---|
| 赛题理解 | Basic/advanced requirements, constraints, test conditions, and scoring items are extracted accurately. |
| 方案论证 | At least two schemes, rejection reasons, and final choice rationale. |
| 工程可行性 | The plan fits common components, team skills, and limited contest time. |
| 系统架构 | Signal flow, control flow, power flow, debug flow, and module responsibilities are clear. |
| 模块复现性 | Each key module has input/output, parts, parameters, risks, debug method, and evidence. |
| 理论分析 | Formulas include variables, substituted values, and design meaning. |
| 硬件设计 | Components have alternatives, risks, protection, and test points. |
| 软件设计 | Main loop, modules, algorithms, timing, interrupts/state machines, fault handling, and debug outputs are readable. |
| 调试计划 | Unit, interface, integration, stress, and pre-judge stages have pass criteria. |
| 测试方案 | Instruments, conditions, steps, repeated trials, data table, error formula, and pass/fail criteria are present. |
| 证据闭环 | Every major metric maps to design implementation and test evidence. |
| 报告规范 | Clear sections, figure/table labels, concise language, and page budget control. |
| 诚信边界 | No fabricated measured data and no rule-violating external assistance. |

## Anonymous Report Checks

Search for:

- 学校、学院、大学、实验室、指导教师
- 姓名、学号、队号、参赛队、联系方式、邮箱、电话
- Source code comments, screenshot paths, file metadata, watermark, EXIF, Git remote names
- Distinctive lab names, teacher names, or team nicknames

When rewriting, replace identity content with neutral descriptions such as“本队”“系统”“作品”.

## Report Health Checklist

High-risk missing items:

- No scheme comparison
- No system block diagram or module responsibilities
- No signal/control/power/debug flow
- No module design cards for key modules
- No theory calculation tied to design decisions
- Hardware and software not both described
- No staged debugging plan
- No instruments/conditions/steps
- No measured data table, or claims success without measured data
- No metric fulfillment matrix linking requirements to test evidence
- No error analysis
- Identity information in anonymous report
- Page limit ignored

## Publish-Ready Skill Checks

Before packaging the skill for GitHub or release:

1. Run `python scripts/skill_self_check.py .` inside the skill folder.
2. Run `python -m unittest discover -s scripts/tests`.
3. Run `python scripts/report_score_checker.py <sample-report.md> --format json` on at least one clean and one problematic sample.
4. Confirm `SKILL.md` stays concise, references are one level deep, and README/LICENSE live in the repository root rather than inside the skill folder.

## Language Standard

Prefer:

- “采用 12 位 ADC 时理论分辨率约 0.806 mV，可满足 5 mV 分辨率要求。”
- “在 5 V 供电、10 Ω 负载条件下记录输出电压和纹波，重复 3 次。”
- “误差主要来自参考电压偏差、采样噪声和仪表读数误差。”

Avoid:

- “本方案简单可靠。”
- “测试结果很好。”
- “系统具有较高创新性。”
- “所有指标均满足要求。” when no measured table is provided.
