# Electronics Reference

Use this reference for quick engineering patterns. Always adapt to the actual problem statement, component limits, and measured data.

## Task-Type Map

| Type | Core evidence | Common risks |
|---|---|---|
| 电源类 | 输出范围、效率、纹波、负载调整率、保护、热 | 发热、纹波、环路稳定、器件余量 |
| 信号测量类 | 量程、分辨率、采样率、误差、校准 | 参考电压、输入保护、噪声、接地 |
| 控制/小车类 | 控制策略、传感器、执行机构、路径/速度测试 | 机械偏差、供电压降、闭环参数 |
| 通信类 | 距离、误码/丢包、协议、抗干扰 | 天线/布线、电源噪声、同步 |
| 传感检测类 | 传感器选择、阈值/算法、环境鲁棒性 | 标定、漂移、干扰、误检 |
| 信号处理/FPGA | 带宽、延迟、采样、资源占用 | 时钟、位宽、同步、测试激励 |

## Hardware Selection Prompts

| Module | Candidate content | Required reasoning |
|---|---|---|
| 主控 | STM32, MSP430, MSPM0, Arduino, ESP32, FPGA | ADC位数、定时器/PWM、串口、功耗、资料和团队熟悉度 |
| 信号采集 | ADC、传感器、分压、运放缓冲、滤波 | 量程、参考电压、采样率、输入保护、抗干扰 |
| 执行控制 | MOS、继电器、H桥、电机驱动、舵机 | 电流余量、反电动势、散热、电源隔离 |
| 显示交互 | OLED、LCD1602、TFT、按键、编码器 | 刷新率、总线占用、调试便利性 |
| 通信 | UART、I2C、SPI、蓝牙、无线模块 | 协议稳定性、丢包、波特率、共地 |
| 电源 | LDO、BUCK、BOOST、电池、保护 | 纹波、效率、压降、限流、反接、散热 |

## Formula Snippets

| Category | Formula | Design meaning |
|---|---|---|
| ADC 分辨率 | `ΔU = Vref / (2^N - 1)` | 判断电压分辨率是否满足精度要求 |
| RC 滤波 | `fc = 1 / (2πRC)` | 选择截止频率，平衡响应速度和抗干扰 |
| 同相运放增益 | `Av = 1 + Rf/Rg` | 设置信号调理放大倍数 |
| 反相运放增益 | `Av = -Rf/Rin` | 设置信号反相放大倍数 |
| PWM | `D = Ton / T` | 解释功率、电机、舵机或亮度控制 |
| 效率 | `η = Pout / Pin × 100%` | 评估电源转换和发热 |
| 相对误差 | `Error = |实测值 - 理论值| / 理论值 × 100%` | 判断测试结果是否满足指标 |

Example:

```markdown
若 ADC 为 12 位，参考电压为 3.3 V，则最小分辨电压为：
ΔU = 3.3 / (2^12 - 1) = 3.3 / 4095 ≈ 0.806 mV。
该结果用于判断测量分辨率是否满足题目精度要求。
```

## Software Flow Skeleton

```text
main():
    SystemClock_Config()
    GPIO_Init()
    ADC_Init()
    PWM_Init()
    UART_Init()
    Display_Init()

    while True:
        raw = Sensor_Read()
        value = Filter_Process(raw)
        control = Control_Update(value)
        Actuator_Output(control)
        Display_Update(value, control)
        UART_Debug_Send(value, control)
```

Report the software by module instead of dumping large code blocks:

| Module | Function | Report wording |
|---|---|---|
| 初始化 | 时钟、GPIO、ADC、PWM、串口、显示 | 说明外设作用和关键参数 |
| 采样 | 周期性读取传感器/输入 | 说明采样频率、通道和触发方式 |
| 滤波 | 均值、中值、一阶低通、卡尔曼 | 说明选择理由和稳定性影响 |
| 控制 | 阈值、PID、状态机、闭环 | 说明输入、输出、关键参数 |
| 显示通信 | OLED、串口、蓝牙 | 说明刷新周期、协议和调试用途 |

## Common Debug Issues

| Symptom | Likely causes | Checks |
|---|---|---|
| ADC 数据跳动 | 参考电压不稳、输入悬空、滤波不足、地线干扰 | 查电源纹波、加输入保护/RC、做均值或中值滤波 |
| OLED 闪烁 | 刷新过快、整屏清屏、I2C 不稳定 | 降低刷新率、局部刷新、检查上拉和线长 |
| 小车跑偏 | 电机差异、PWM 不一致、轮胎摩擦、供电压降 | 左右轮标定、闭环反馈、速度补偿 |
| 电源发热 | 压差/电流过大、散热不足、线性损耗高 | 测输入输出功率、改 BUCK、加散热 |
| 串口乱码 | 波特率不一致、未共地、时钟配置错误 | 统一波特率、检查时钟、确保共地 |
| 电机干扰复位 | 反电动势、电源跌落、地线耦合 | 加续流/TVS、电源分区、粗线回流、复位上拉 |

## Safety Reminders

- 电源类: include fuse/current limit, reverse polarity, thermal, load, and discharge notes.
- 锂电池: include overcharge/overdischarge/short-circuit protection and charging safety.
- 电机/继电器: include flyback paths, isolation, and stall current margin.
- 高压/市电: recommend isolation, enclosure, one-hand rule, and teacher/lab supervision.
- 无线: remind the user to follow local radio rules and contest module restrictions.
