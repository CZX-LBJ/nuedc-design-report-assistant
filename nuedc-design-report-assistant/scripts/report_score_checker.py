#!/usr/bin/env python3
"""Conservative Markdown health checker for NUEDC-style design reports."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    {
        "id": "missing-abstract",
        "label": "摘要",
        "patterns": [r"(^|\n)#{1,4}\s*摘要\b", r"\n摘要[:：]"],
        "severity": "medium",
        "message": "缺少摘要或摘要标题不清晰。",
    },
    {
        "id": "missing-keywords",
        "label": "关键词",
        "patterns": [r"关键词"],
        "severity": "low",
        "message": "缺少关键词。",
    },
    {
        "id": "missing-system-scheme",
        "label": "系统方案",
        "patterns": [r"系统方案", r"总体方案", r"系统总体", r"方案比较"],
        "severity": "high",
        "message": "缺少系统方案/总体方案部分。",
    },
    {
        "id": "missing-theory",
        "label": "理论分析",
        "patterns": [r"理论分析", r"参数计算", r"公式", r"分辨率", r"误差计算"],
        "severity": "high",
        "message": "缺少理论分析或关键参数计算。",
    },
    {
        "id": "missing-hardware-software",
        "label": "电路与程序",
        "patterns": [r"电路.*程序", r"硬件.*软件", r"程序设计", r"软件流程"],
        "severity": "high",
        "message": "缺少硬件电路与软件流程说明。",
    },
    {
        "id": "missing-test-plan",
        "label": "测试方案",
        "patterns": [r"测试方案", r"测试仪器", r"测试条件", r"测试步骤"],
        "severity": "high",
        "message": "缺少测试方案、测试仪器、测试条件或测试步骤。",
    },
    {
        "id": "missing-error-analysis",
        "label": "误差分析",
        "patterns": [r"误差分析", r"误差来源", r"相对误差"],
        "severity": "medium",
        "message": "缺少误差分析。",
    },
    {
        "id": "missing-summary",
        "label": "总结",
        "patterns": [r"(^|\n)#{1,4}\s*(五、)?总结\b", r"\n总结[:：]"],
        "severity": "low",
        "message": "缺少总结。",
    },
]

IDENTITY_PATTERNS = [
    r"学校[:：]",
    r"学院[:：]",
    r"大学",
    r"姓名[:：]",
    r"学号[:：]",
    r"队号[:：]",
    r"参赛队",
    r"指导教师",
    r"电话[:：]",
    r"邮箱[:：]",
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
]

PLACEHOLDER_PATTERNS = [r"待填写", r"TBD", r"TODO", r"xx+", r"XX+", r"__+"]


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def add_issue(issues: list[dict], issue_id: str, severity: str, message: str, evidence: str = "") -> None:
    issues.append(
        {
            "id": issue_id,
            "severity": severity,
            "message": message,
            "evidence": evidence[:160],
        }
    )


def count_chinese_abstract_chars(text: str) -> int | None:
    match = re.search(r"(?:^|\n)#{1,4}\s*摘要\s*\n(?P<body>.*?)(?=\n#{1,4}\s|\Z)", text, re.S)
    if not match:
        match = re.search(r"摘要[:：]\s*(?P<body>.*?)(?=\n\s*(关键词|一、|#)|\Z)", text, re.S)
    if not match:
        return None
    body = re.sub(r"[#|`\-\s]", "", match.group("body"))
    return len(body)


def has_real_measurement_table(text: str) -> bool:
    has_table = "|" in text and "---" in text
    required_terms = all(term in text for term in ("理论值", "实测值", "误差"))
    has_numeric_measurement = bool(re.search(r"\|\s*\d+[^|\n]*\|[^|\n]*\d", text))
    return has_table and required_terms and has_numeric_measurement


def has_pending_measurement_table(text: str) -> bool:
    has_table = "|" in text and "---" in text
    required_terms = all(term in text for term in ("理论值", "实测值", "误差"))
    pending_terms = any(term in text for term in ("待填写", "待实测", "待测", "待现场复测"))
    return has_table and required_terms and pending_terms


def analyze(text: str, source: str, max_pages: int, chars_per_page: int) -> dict:
    issues: list[dict] = []
    normalized = compact(text)

    for section in REQUIRED_SECTIONS:
        if not has_any(text, section["patterns"]):
            add_issue(issues, section["id"], section["severity"], section["message"])

    scheme_markers = re.findall(r"方案[一二三四五六\d]", text)
    has_final_choice = bool(re.search(r"最终(方案)?选择|推荐选择|选择理由", text))
    if len(set(scheme_markers)) < 2 or not has_final_choice:
        add_issue(
            issues,
            "missing-scheme-comparison",
            "high",
            "方案论证不足：至少需要两套方案、比较维度和最终选择理由。",
            "；".join(sorted(set(scheme_markers))) or "未发现方案一/方案二等标记",
        )

    has_real_data = has_real_measurement_table(text)
    has_pending_data = has_pending_measurement_table(text)

    if not has_real_data and has_pending_data:
        add_issue(
            issues,
            "test-data-pending",
            "medium",
            "发现待填写/待实测测试表。该写法合规，但提交或结论判断前必须补入真实实测数据。",
        )
    elif not has_real_data:
        add_issue(
            issues,
            "missing-test-data",
            "high",
            "未发现包含理论值、实测值、误差的测试数据表。没有数据时应保留待填写表格。",
        )

    unsupported_claim = re.search(r"(测试结果|所有指标|各项指标|实物测试).{0,20}(符合|达到|满足|成功|良好)", normalized)
    if unsupported_claim and not has_real_data:
        add_issue(
            issues,
            "claim-without-measured-data",
            "high",
            "存在测试成功/指标满足类表述，但缺少实测数据表支撑。",
            unsupported_claim.group(0),
        )

    for pattern in IDENTITY_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            add_issue(
                issues,
                "identity-risk",
                "high",
                "报告可能包含匿名评审不应出现的身份信息。",
                match.group(0),
            )
            break

    for pattern in PLACEHOLDER_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            add_issue(
                issues,
                "placeholder-present",
                "medium",
                "报告仍包含占位符，提交前需要替换或明确标注为待测。",
                match.group(0),
            )
            break

    char_count = len(re.sub(r"\s+", "", text))
    approx_pages = max(1, math.ceil(char_count / chars_per_page))
    if approx_pages > max_pages:
        add_issue(
            issues,
            "page-budget-risk",
            "medium",
            f"按 {chars_per_page} 字/页粗略估计约 {approx_pages} 页，可能超过 {max_pages} 页正文预算。",
        )

    abstract_chars = count_chinese_abstract_chars(text)
    if abstract_chars is not None and abstract_chars > 300:
        add_issue(
            issues,
            "abstract-too-long",
            "medium",
            f"摘要约 {abstract_chars} 字，常见要求是 300 字以内；请以当年/赛区规则为准。",
        )

    risk_counts = {"high": 0, "medium": 0, "low": 0}
    for issue in issues:
        risk_counts[issue["severity"]] += 1

    return {
        "source": source,
        "metrics": {
            "characters_no_whitespace": char_count,
            "approx_pages": approx_pages,
            "max_pages": max_pages,
            "chars_per_page": chars_per_page,
            "abstract_chars": abstract_chars,
        },
        "risk_counts": risk_counts,
        "issues": issues,
    }


def print_text_report(result: dict) -> None:
    metrics = result["metrics"]
    print(f"Report: {result['source']}")
    print(
        "Approx size: "
        f"{metrics['characters_no_whitespace']} chars, "
        f"{metrics['approx_pages']} pages "
        f"(budget {metrics['max_pages']} pages)"
    )
    counts = result["risk_counts"]
    print(f"Risks: high={counts['high']} medium={counts['medium']} low={counts['low']}")
    if not result["issues"]:
        print("No obvious NUEDC report health issues found.")
        return
    print()
    for issue in result["issues"]:
        evidence = f" Evidence: {issue['evidence']}" if issue["evidence"] else ""
        print(f"- [{issue['severity']}] {issue['id']}: {issue['message']}{evidence}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Markdown report to check")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--max-pages", type=int, default=8)
    parser.add_argument("--chars-per-page", type=int, default=1100)
    parser.add_argument("--strict", action="store_true", help="exit 1 when high-risk issues are found")
    args = parser.parse_args(argv)

    text = read_text(args.report)
    result = analyze(text, str(args.report), args.max_pages, args.chars_per_page)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text_report(result)

    if args.strict and result["risk_counts"]["high"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
