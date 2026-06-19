import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "report_score_checker.py"


def run_checker(markdown: str, *args: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.md"
        report.write_text(markdown, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(report), "--format", "json", *args],
            check=True,
            text=True,
            capture_output=True,
        )
    return json.loads(result.stdout)


def run_checker_process(markdown: str, *args: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.md"
        report.write_text(markdown, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(report), "--format", "json", *args],
            text=True,
            capture_output=True,
        )


class ReportScoreCheckerTests(unittest.TestCase):
    def test_flags_missing_core_sections_and_identity_risk(self):
        output = run_checker(
            """
# 简易报告

学校：某某大学
姓名：张三

本作品采用 STM32 实现，测试结果均符合要求。
"""
        )

        issue_ids = {issue["id"] for issue in output["issues"]}
        self.assertIn("identity-risk", issue_ids)
        self.assertIn("missing-scheme-comparison", issue_ids)
        self.assertIn("missing-test-data", issue_ids)
        self.assertGreaterEqual(output["risk_counts"]["high"], 3)

    def test_accepts_complete_markdown_report_with_real_measurement_table(self):
        output = run_checker(
            """
# 设计报告

## 摘要
本系统完成电压测量任务，采用 STM32、运放调理和 OLED 显示。

## 关键词
电压测量；ADC；误差分析

## 一、系统方案
### 方案比较与选择
方案一：采用 STM32 内置 ADC。方案二：采用外置 ADS1115。
最终选择方案二，因为分辨率更高，调试风险可控。

## 二、理论分析与参数计算
ADC 分辨率：ΔU = Vref / (2^N - 1)。

## 三、电路与程序设计
硬件包含输入保护、信号调理、ADC、主控和显示模块。
软件包含初始化、采样、滤波、显示和串口调试模块。

## 四、测试方案与测试结果
测试仪器：直流稳压电源、万用表。
测试条件：5V 供电，室温，重复测试 3 次。

| 测试序号 | 理论值 | 实测值 | 误差 | 是否满足 |
|---|---:|---:|---:|---|
| 1 | 1.000V | 1.003V | 0.30% | 是 |
| 2 | 2.000V | 2.006V | 0.30% | 是 |

## 误差分析
误差主要来自参考电压偏差、万用表读数和运放失调。

## 指标完成情况
| 题目要求 | 设计实现 | 测试项目 | 测试结果 | 是否满足 |
|---|---|---|---|---|
| 1V 与 2V 电压测量 | 外置 ADC 采样 | 逐点输入测试 | 最大误差 0.30% | 是 |

## 五、总结
作品达到基本要求，后续可优化参考源和输入保护。
"""
        )

        self.assertEqual(output["risk_counts"]["high"], 0)
        self.assertFalse(
            any(issue["id"] == "missing-test-data" for issue in output["issues"])
        )

    def test_accepts_pending_test_table_without_fabricated_measurements(self):
        output = run_checker(
            """
# 设计报告

## 摘要
本系统拟完成信号测量任务，采用信号调理、ADC 采样和 OLED 显示。

## 关键词
信号测量；ADC；测试方案

## 一、系统方案
### 方案比较与选择
方案一：采用 STM32 内置 ADC。方案二：采用外置高精度 ADC。
最终选择方案二，因为分辨率更高，便于满足精度指标。

## 二、理论分析与参数计算
ADC 分辨率：ΔU = Vref / (2^N - 1)。

## 三、电路与程序设计
硬件包含输入保护、信号调理、ADC、主控和显示模块。
软件包含初始化、采样、滤波、显示和串口调试模块。

## 四、测试方案与测试结果
测试仪器：万用表、信号发生器、示波器。
测试条件：待实测填写。测试步骤：逐点输入并记录输出。

| 测试序号 | 输入值 | 理论值 | 实测值 | 误差 | 是否满足要求 |
|---|---|---|---|---|---|
| 1 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 |

## 误差分析
误差可能来自参考电压、采样噪声和仪表读数。

## 五、总结
当前报告保留待实测测试表，实测后再判断是否满足指标。
"""
        )

        issue_ids = {issue["id"] for issue in output["issues"]}
        self.assertNotIn("missing-test-data", issue_ids)
        self.assertIn("test-data-pending", issue_ids)
        self.assertEqual(output["risk_counts"]["high"], 0)

    def test_flags_success_claim_when_only_pending_test_table_exists(self):
        output = run_checker(
            """
# 设计报告

## 摘要
本系统采用 STM32 进行电压测量，测试结果均满足要求。

## 关键词
电压测量；ADC；误差分析

## 一、系统方案
### 方案比较与选择
方案一：采用 STM32 内置 ADC。方案二：采用外置 ADC。
最终选择方案二。

## 二、理论分析与参数计算
ADC 分辨率：ΔU = Vref / (2^N - 1)。

## 三、电路与程序设计
硬件包含输入保护、信号调理、ADC、主控和显示模块。
软件包含初始化、采样、滤波、显示和串口调试模块。

## 四、测试方案与测试结果
测试仪器：万用表。测试条件：待填写。测试步骤：待填写。

| 测试序号 | 理论值 | 实测值 | 误差 | 是否满足要求 |
|---|---|---|---|---|
| 1 | 待填写 | 待填写 | 待填写 | 待填写 |

## 误差分析
误差待实测后分析。

## 五、总结
作品达到基本要求。
"""
        )

        issue_ids = {issue["id"] for issue in output["issues"]}
        self.assertIn("claim-without-measured-data", issue_ids)
        self.assertGreaterEqual(output["risk_counts"]["high"], 1)

    def test_pending_fulfillment_table_header_is_not_success_claim(self):
        output = run_checker(
            """
# 设计报告

## 摘要
本系统拟完成信号测量任务，采用信号调理、ADC 采样和显示模块。当前仅保留测试表，实测后再判断指标。

## 关键词
信号测量；ADC；测试方案

## 一、系统方案
### 方案比较与选择
方案一：采用 STM32 内置 ADC。方案二：采用外置高精度 ADC。
最终选择方案二，因为分辨率更高，便于满足精度指标。

## 二、理论分析与参数计算
ADC 分辨率：ΔU = Vref / (2^N - 1)。

## 三、电路与程序设计
硬件包含输入保护、信号调理、ADC、主控和显示模块。
软件包含初始化、采样、滤波、显示和串口调试模块。

## 四、测试方案与测试结果
测试仪器：万用表、信号发生器、示波器。
测试条件：待实测填写。测试步骤：逐点输入并记录输出。

| 测试序号 | 输入值 | 理论值 | 实测值 | 误差 | 是否满足要求 |
|---|---|---|---|---|---|
| 1 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 |

## 误差分析
误差可能来自参考电压、采样噪声和仪表读数。

## 指标完成情况
| 题目要求 | 设计实现 | 测试项目 | 测试结果 | 误差/得分依据 | 是否满足 |
|---|---|---|---|---|---|
| 信号幅值测量 | 外置 ADC 采样 | 标准信号测试 | 待实测 | 待计算 | 待判断 |

## 五、总结
当前报告保留待实测测试表，实测后再判断是否满足指标。
"""
        )

        self.assertNotIn(
            "claim-without-measured-data",
            {issue["id"] for issue in output["issues"]},
        )

    def test_strict_exits_nonzero_for_high_risk_report(self):
        result = run_checker_process(
            """
# 简易报告

学校：某某大学
测试结果均符合要求。
""",
            "--strict",
        )

        self.assertNotEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        self.assertGreater(output["risk_counts"]["high"], 0)

    def test_flags_abstract_over_300_chars(self):
        long_abstract = "本系统" + ("完成信号测量任务。" * 80)
        output = run_checker(
            f"""
# 设计报告

## 摘要
{long_abstract}

## 关键词
信号测量；ADC；误差分析

## 一、系统方案
### 方案比较与选择
方案一：采用 STM32 内置 ADC。方案二：采用外置 ADC。
最终选择方案二。

## 二、理论分析与参数计算
ADC 分辨率：ΔU = Vref / (2^N - 1)。

## 三、电路与程序设计
硬件包含输入保护、信号调理、ADC、主控和显示模块。
软件包含初始化、采样、滤波、显示和串口调试模块。

## 四、测试方案与测试结果
测试仪器：万用表。测试条件：5V 供电。测试步骤：逐点测试。

| 测试序号 | 理论值 | 实测值 | 误差 | 是否满足要求 |
|---|---:|---:|---:|---|
| 1 | 1.000V | 1.002V | 0.20% | 是 |

## 误差分析
误差主要来自参考电压。

## 五、总结
作品达到基本要求。
"""
        )

        self.assertIn("abstract-too-long", {issue["id"] for issue in output["issues"]})

    def test_flags_missing_metric_fulfillment_matrix_for_detailed_report(self):
        output = run_checker(
            """
# 设计报告

## 摘要
本系统完成电压测量任务，采用 STM32、运放调理和 OLED 显示。

## 关键词
电压测量；ADC；误差分析

## 一、系统方案
### 方案比较与选择
方案一：采用 STM32 内置 ADC。方案二：采用外置 ADS1115。
最终选择方案二，因为分辨率更高，调试风险可控。

## 二、理论分析与参数计算
ADC 分辨率：ΔU = Vref / (2^N - 1)。

## 三、电路与程序设计
硬件包含输入保护、信号调理、ADC、主控和显示模块。
软件包含初始化、采样、滤波、显示和串口调试模块。

## 四、测试方案与测试结果
测试仪器：直流稳压电源、万用表。
测试条件：5V 供电，室温，重复测试 3 次。

| 测试序号 | 理论值 | 实测值 | 误差 | 是否满足 |
|---|---:|---:|---:|---|
| 1 | 1.000V | 1.003V | 0.30% | 是 |
| 2 | 2.000V | 2.006V | 0.30% | 是 |

## 误差分析
误差主要来自参考电压偏差、万用表读数和运放失调。

## 五、总结
作品达到基本要求，后续可优化参考源和输入保护。
"""
        )

        self.assertIn(
            "missing-metric-fulfillment-matrix",
            {issue["id"] for issue in output["issues"]},
        )


if __name__ == "__main__":
    unittest.main()
