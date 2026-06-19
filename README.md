# NUEDC Design & Report Assistant

电赛设计方案与报告助手是一个面向全国大学生电子设计竞赛、TI 杯、省赛、校赛和电子类课程设计的 Codex skill。它的目标不是代做电赛，而是在合规边界内辅助完成完整工程流程：赛题拆解、选题与方案论证、系统架构、硬件/软件/算法设计、理论计算、分阶段调试、测试验证、设计报告生成与报告体检。

## 适用场景

- 赛前训练、校内模拟赛、课程设计和赛后复盘
- 将已有方案、调试记录和真实测试数据整理为规范设计报告
- 对报告做评分点、匿名信息、页数和测试证据检查
- 为指导教师或实验室建立统一的电赛训练报告规范
- 用公开真题做赛前训练，按“省级一等奖水平”做工程闭环演练

正式竞赛期间请遵守当年官方规则和所在赛区细则。本项目不鼓励、不支持队外代做、代写或任何违反独立完成要求的使用方式。

## 核心能力

- 赛题解析：拆解基本要求、发挥部分、限制条件、测试方式和风险
- 方案论证：生成 2-4 套方案并按难度、稳定性、指标潜力和调试风险比较
- 系统设计：输出信号流、控制流、电源流、调试流、模块设计卡和 Mermaid 框图建议
- 硬件/软件/算法设计：给出选型理由、替代方案、关键参数、程序流程、状态机、伪代码和调试接口
- 理论计算：把公式绑定到 ADC 分辨率、滤波、增益、PWM、效率、误差等设计决策
- 分阶段调试：规划单模块、接口、集成、压力测试和赛前复测路径
- 测试方案：生成测试仪器、条件、步骤、重复试验、数据表、误差计算和复测说明
- 报告体检：检查缺项、匿名风险、假实测数据、摘要长度和页数预算

## 质量目标

当用户要求“非常完善”“获奖级别”“省一水平”时，skill 默认按全流程高标准输出：

```text
指标 -> 方案 -> 模块 -> 调试 -> 测试 -> 报告
```

它不会承诺获奖，因为最终成绩取决于实物实现、现场测试、队伍执行和官方评分。但它会把输出拉到接近省级一等奖训练所需的工程粒度：需求矩阵、方案比较、模块设计卡、关键计算、硬件保护、软件状态机、分阶段调试、测试证据矩阵和指标完成情况表。

## 安装

将 skill 文件夹复制到 Codex skills 目录：

```powershell
Copy-Item -Recurse .\nuedc-design-report-assistant "$env:USERPROFILE\.codex\skills\"
```

然后在新对话里使用：

```text
Use $nuedc-design-report-assistant to analyze this NUEDC problem and produce a design plan.
```

## 仓库结构

```text
nuedc-design-report-assistant-open-source/
├── README.md
├── LICENSE
├── examples/
│   ├── report-clean.md
│   ├── report-pending-test.md
│   ├── report-with-issues.md
│   └── validation-2023-e-award-level-workflow.md
├── .github/workflows/validate.yml
└── nuedc-design-report-assistant/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    └── scripts/
```

## 测试

```bash
python nuedc-design-report-assistant/scripts/skill_self_check.py nuedc-design-report-assistant
python -m unittest discover -s nuedc-design-report-assistant/scripts/tests
python nuedc-design-report-assistant/scripts/report_score_checker.py examples/report-clean.md --strict
```

问题报告在严格模式下应该失败：

```bash
python nuedc-design-report-assistant/scripts/report_score_checker.py examples/report-with-issues.md --strict
```

待实测报告会通过“缺失测试表”检查，但会提示 `test-data-pending`，表示不能据此宣称指标已满足。

端到端验证样例：

```bash
python - <<'PY'
from pathlib import Path
text = Path("examples/validation-2023-e-award-level-workflow.md").read_text(encoding="utf-8")
required = ["赛题拆解与需求矩阵", "方案论证", "系统总体架构", "模块设计卡", "分阶段调试计划", "测试证据矩阵", "指标完成情况"]
missing = [item for item in required if item not in text]
raise SystemExit(f"missing sections: {missing}" if missing else 0)
PY
```

## 资料依据

本 skill 的合规边界和报告结构参考公开资料抽象而来，不复制优秀作品内容：

- 全国大学生电子设计竞赛培训网：《2025年全国大学生电子设计竞赛实施过程说明》  
  https://www.nuedc-training.com.cn/index/news/details/new_id/333
- TI：《全国大学生电子设计竞赛章程》  
  https://www.ti.com.cn/cn/lit/pdf/zhcn003
- 上海赛区：《2025年TI杯全国大学生电子设计竞赛上海赛区实施过程说明》  
  https://nuedc-sh.sjtu.edu.cn/post_detail.php?id=42
- 全国大学生电子设计竞赛获奖作品选编示例  
  https://www.nuedcchina.com/upload/201905/bb1945dac213c3344eb72399e1ae9767.pdf
- 2023 年 E 题公开题目：运动目标控制与自动追踪系统
  https://nuedc.org/problems/2023_E%E9%A2%98_%E8%BF%90%E5%8A%A8%E7%9B%AE%E6%A0%87%E6%8E%A7%E5%88%B6%E4%B8%8E%E8%87%AA%E5%8A%A8%E8%BF%BD%E8%B8%AA%E7%B3%BB%E7%BB%9F.pdf

规则会随年份和赛区变化，最终提交前应以当年官方通知为准。

## License

MIT License. See `LICENSE`.
