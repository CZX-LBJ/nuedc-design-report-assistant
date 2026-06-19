# NUEDC Design & Report Assistant

电赛设计方案与报告助手是一个面向全国大学生电子设计竞赛、TI 杯、省赛、校赛和电子类课程设计的 Codex skill。它的目标不是代做电赛，而是帮助参赛者在合规边界内完成工程化流程：赛题解析、方案论证、硬件/软件设计、理论计算、测试方案、测试数据整理、设计报告生成与报告体检。

## 适用场景

- 赛前训练、校内模拟赛、课程设计和赛后复盘
- 将已有方案、真实测试数据整理为规范设计报告
- 对报告做评分点、匿名信息、页数和测试证据检查
- 为指导教师或实验室建立统一的电赛训练报告规范

正式竞赛期间请遵守当年官方规则和所在赛区细则。本项目不鼓励、不支持队外代做、代写或任何违反独立完成要求的使用方式。

## 核心能力

- 赛题解析：拆解基本要求、发挥部分、限制条件、测试方式和风险
- 方案论证：生成 2-4 套方案并按难度、稳定性、指标潜力和调试风险比较
- 系统设计：输出模块、信号流、控制流、电源流、接口和 Mermaid 框图建议
- 硬件/软件设计：给出选型理由、替代方案、程序流程、伪代码和调试接口
- 理论计算：把公式绑定到 ADC 分辨率、滤波、增益、PWM、效率、误差等设计决策
- 测试方案：生成测试仪器、条件、步骤、数据表、误差计算和复测说明
- 报告体检：检查缺项、匿名风险、假实测数据、摘要长度和页数预算

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
│   └── report-with-issues.md
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

规则会随年份和赛区变化，最终提交前应以当年官方通知为准。

## License

MIT License. See `LICENSE`.
