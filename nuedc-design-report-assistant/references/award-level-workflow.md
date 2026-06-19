# Award-Level NUEDC Workflow

Use this reference when the user wants full-process NUEDC help, not only report writing. The target is a provincial-first-prize-level training workflow: accurate problem parsing, feasible engineering choices, disciplined debugging, reproducible tests, and a report that preserves the evidence chain. Do not promise awards; use "省级一等奖水平" only as a quality target.

## Core Standard

The whole skill should enforce this chain:

`指标-方案-模块-调试-测试-报告`

Every important output must answer five questions:

1. Which problem requirement or scoring point does this serve?
2. Which scheme or module implements it?
3. Which parameter, formula, circuit, algorithm, or control logic makes it credible?
4. How will the team debug and verify it before final testing?
5. Which table, waveform, measurement, or conclusion will enter the report?

If any answer is missing, mark it as `待补充` or `待实测`, not as completed.

## Full Workflow

### 1. Usage Boundary And Contest Phase

Classify the request first:

| Phase | Allowed help | Refuse or limit |
|---|---|---|
| 赛前训练 | Full analysis, design, code skeletons, tests, report templates | None beyond safety and honesty |
| 校赛/课程设计 | Full learning-oriented assistance | Do not fabricate real measurements |
| 赛后复盘 | Full reconstruction and report polish from real data | Do not rewrite history or invent data |
| 正式赛期 | Rules, safety, checklists, generic study guidance | Do not provide outside solving, design, code, or report writing that violates independence |

When the user is likely in a live official contest, ask for context if needed and keep help inside current rules.

### 2. 赛题拆解

Always build a requirement matrix before proposing a design.

| Field | What to extract |
|---|---|
| 任务目标 | What the system must do in one sentence |
| 基本要求 | Required functions and minimum metrics |
| 发挥部分 | Higher-score functions, precision, speed, robustness, automation |
| 测试条件 | Input range, load, distance, time, environment, instruments |
| 限制条件 | Size, power, components, no-network rules, allowed boards |
| 隐性风险 | Heat, noise, calibration, mechanical error, safety, test repeatability |
| Scoring leverage | Which items likely decide ranking |

Then produce:

1. `P0`: must finish to pass basic requirements.
2. `P1`: high-score items with realistic implementation path.
3. `P2`: bonus or polish items that must not endanger P0/P1.

### 3. Topic-Type Diagnosis

Classify the task into one or more types and choose the evidence strategy.

| Type | Design center | Evidence center |
|---|---|---|
| 电源/电力电子 | topology, switch devices, feedback, protection, thermal | voltage/current range, efficiency, ripple, load regulation, protection |
| 测量仪器 | signal chain, reference, ADC, calibration, filtering | range, resolution, error, repeatability, calibration curve |
| 信号源/信号处理 | waveform generation, timing, bandwidth, spectrum | frequency error, amplitude error, THD, spectrum, response |
| 控制/小车/运动 | sensing, actuator, control loop, mechanics | path/position/speed/time, repeated trials, failure modes |
| 通信/无线 | modulation, protocol, synchronization, antenna, anti-interference | distance, BER/PER, latency, robustness |
| 视觉/智能感知 | optics, sensor, algorithm, compute budget | detection accuracy, latency, lighting robustness |
| Mixed embedded system | interfaces, scheduling, state machine, fault handling | end-to-end functional tests and module tests |

### 4. Scheme Generation And 方案论证

For a provincial-first-prize-level workflow, do not stop at "方案一/方案二". Compare schemes by contest survival value.

Required comparison dimensions:

- 指标上限: can it meet basic and advanced metrics?
- 稳定性: noise, heat, mechanical tolerance, algorithm sensitivity.
- 调试速度: can the team isolate faults within hours?
- 器件可获得性: available parts, replacements, datasheets.
- 测试可复现: can the result be measured repeatedly by judges?
- Team fit: known MCU/FPGA/analog/software skills.
- Failure cost: what happens if this scheme partially fails?

A good final choice sentence should follow:

`综合[核心指标]、[调试风险]、[器件/团队条件]和[测试可复现性]，选择[方案]；放弃[方案]的主要原因是[具体风险]。`

### 5. System Architecture

Build architecture in four flows:

| Flow | Must include |
|---|---|
| 信号流 | sensor/input -> conditioning -> sampling/processing -> output |
| 控制流 | state, feedback, controller, actuator, fail-safe |
| 电源流 | source, rails, current budget, noise isolation, protection |
| 调试流 | serial logs, test points, indicator LEDs, saved parameters |

For every module, write a module design card:

| Field | Content |
|---|---|
| Module name | e.g. signal conditioning |
| Requirement served | Requirement ID or scoring item |
| Input/output | Electrical/logic/mechanical quantities |
| Key parts | Main ICs, sensors, drivers, passives |
| Key parameters | gain, bandwidth, sample rate, current, resolution |
| Risk | likely failure or uncertainty |
| Debug method | test point, waveform, serial variable, calibration step |
| Report evidence | table, waveform, photo, calculation, figure |

### 6. Hardware Design

Hardware help should move from requirements to actual decisions.

Minimum outputs:

- Block diagram and module responsibilities.
- Main components with alternatives and reason for rejection.
- Input protection, filtering, grounding, shielding, heat, current margin.
- Power budget with each rail and estimated current.
- Debug points: TP names, expected voltage/waveform, instrument.
- Assembly risks: connector polarity, mechanical tolerance, cable strain.

For analog and power work, include:

- Reference voltage and calibration plan.
- Noise source analysis and filter cutoff choice.
- Power device voltage/current/thermal margin.
- Protection: fuse, current limit, reverse polarity, TVS/flyback, isolation.

### 7. Software And Algorithm Design

Software output should be implementable, but not pretend to be final code without actual pins and libraries.

Required views:

1. State machine or main loop.
2. Peripheral configuration table: ADC/PWM/timer/UART/I2C/SPI/GPIO.
3. Data pipeline: sampling -> filter -> estimate -> decision/control -> output.
4. Timing budget: sample period, control period, display/log period.
5. Fault handling: timeout, sensor invalid, overcurrent, lost target, reset.
6. Debug protocol: serial variables, log format, calibration commands.

For control tasks, include:

- Open-loop baseline.
- Closed-loop feedback source.
- Controller form: threshold/PID/state machine/feedforward.
- Parameter tuning plan and stop conditions.
- Repeated-trial scoring method.

### 8. Theory, Calculation, Simulation

Only include calculations that decide something.

For each calculation, use this pattern:

`指标需求 -> 公式 -> 代入参数 -> 结果 -> 设计决策 -> 验证方法`

Examples of design-linked calculations:

- ADC resolution and quantization error.
- Sampling theorem and timer period.
- RC/active filter cutoff.
- Amplifier gain and input range.
- PWM frequency and duty ratio resolution.
- Motor torque/current margin.
- Thermal loss and heat-sink need.
- Communication data rate and latency.
- Error propagation and calibration equation.

If simulation is suggested, specify input model, expected output, and what design choice it validates. Do not report simulation as real measurement.

### 9. 分阶段调试

Provincial-first-prize-level work depends on fast isolation. Use staged debugging:

| Stage | Goal | Evidence |
|---|---|---|
| Unit power-on | rails stable, no overheating | voltage/current table |
| Single module | each sensor/driver/signal chain works alone | waveform/log screenshot notes |
| Interface | MCU can read/write each peripheral | serial logs, bus waveform |
| Algorithm offline | algorithm works on recorded or simulated data | error table |
| Integrated loop | closed loop works at low speed/safe load | repeated trial notes |
| Stress test | edge input, long run, disturbances | pass/fail matrix |
| Pre-judge rehearsal | run exact scoring steps | final measurement table |

Debug log template:

| Time | Symptom | Hypothesis | Test | Result | Change | Next step |
|---|---|---|---|---|---|---|
| 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 |

### 10. Test And Evidence Strategy

Every scoring item needs a test card:

| Field | Content |
|---|---|
| Requirement ID | Basic/advanced item |
| Metric | numeric target or functional pass condition |
| Instrument | model/accuracy if known |
| Setup | power, load, distance, signal, environment |
| Procedure | repeatable steps |
| Raw data | table columns |
| Calculation | error, efficiency, response time, success rate |
| Pass/fail | threshold |
| Retest trigger | when to repeat |

Use repeated trials for motion, vision, communication, and unstable analog results. Record failures instead of hiding them; explain the final fix or limitation.

### 11. Time And Team Plan

For a 4-day contest practice, propose a schedule that protects test time:

| Period | Main goal |
|---|---|
| 0-4 h | read problem, choose topic, requirement matrix, final scheme |
| 4-16 h | unit circuits, minimal firmware, mechanical prototype |
| 16-32 h | module integration, logs, first complete demo |
| 32-48 h | advanced metrics, calibration, robustness |
| 48-64 h | scoring rehearsal, fix top failures, write report alongside tests |
| 64-80 h | final measurements, report compression, anonymity and evidence audit |

If P0 is not stable by the midpoint, freeze advanced features and recover basic scoring.

### 12. Output Levels

Offer the user a depth level when needed:

| Level | Use when | Output |
|---|---|---|
| L1 Quick | Choosing a topic or direction | requirement matrix, risks, scheme shortlist |
| L2 Engineering | Building the project | architecture, module cards, calculations, software, debug plan |
| L3 Award-Level | Training for high score | L2 plus scoring strategy, test evidence matrix, schedule, failure modes |
| L4 Report Package | Preparing final materials | full report, 8-page compression, abstract, QA checklist |

Default to L3 when the user asks for "完善", "获奖", "省一", "国奖", or "完整复现".

### 13. End-To-End Validation Prompt

When testing this skill, use a real public problem for 端到端验证 and require the output to include:

1. Requirement/scoring matrix.
2. Topic-type diagnosis.
3. 2-4方案论证.
4. Final architecture with four flows.
5. Module design cards.
6. Key calculations.
7. Hardware, software, and algorithm plan.
8. Staged debugging plan.
9. Test evidence matrix.
10. Report outline and metric fulfillment table.
11. An honesty/compliance audit.

The output is not strong enough if it only gives a report outline, generic component names, or unsupported success claims.
