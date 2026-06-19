#!/usr/bin/env python3
"""Self-check a NUEDC Design & Report Assistant skill folder."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/award-level-workflow.md",
    "references/excellent-report-patterns.md",
    "references/templates.md",
    "references/electronics-reference.md",
    "references/compliance-quality.md",
    "scripts/report_score_checker.py",
    "scripts/skill_self_check.py",
    "scripts/tests/test_report_score_checker.py",
    "scripts/tests/test_skill_self_check.py",
]

MOJIBAKE_MARKERS = [
    "\u951f\u65a4\u62f7",
    "\u00ef\u00bf\u00bd",
    "\u934f\u3125",
    "\u7487\u6d98",
    "\u9422\u57ab",
    "\u93bd\u6a3f",
    "\u701b\ufe41\u725e",
]

REFERENCE_LINKS = [
    "references/award-level-workflow.md",
    "references/excellent-report-patterns.md",
    "references/templates.md",
    "references/electronics-reference.md",
    "references/compliance-quality.md",
    "scripts/report_score_checker.py",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(?P<body>.*?)\n---", text, flags=re.S)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter")

    data: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        if not raw_line.strip() or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_text_file(path: Path, root: Path, errors: list[str]) -> None:
    try:
        text = read_text(path)
    except UnicodeDecodeError as exc:
        errors.append(f"{path.relative_to(root).as_posix()} is not valid UTF-8: {exc}")
        return
    if "\ufffd" in text:
        errors.append(f"{path.relative_to(root).as_posix()} contains replacement characters")
    for marker in MOJIBAKE_MARKERS:
        if marker in text:
            errors.append(
                f"{path.relative_to(root).as_posix()} contains likely mojibake marker {marker!r}"
            )
            break


def analyze(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    metrics: dict[str, int | str] = {"root": str(root)}

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".yaml", ".yml"}:
            check_text_file(path, root, errors)

    skill_md = root / "SKILL.md"
    if skill_md.is_file():
        text = read_text(skill_md)
        metrics["skill_lines"] = text.count("\n") + 1
        metrics["skill_bytes"] = skill_md.stat().st_size
        try:
            frontmatter = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(str(exc))
            frontmatter = {}

        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        metrics["description_chars"] = len(description)
        if not name:
            errors.append("SKILL.md frontmatter missing name")
        elif not re.fullmatch(r"[a-z0-9-]{1,63}", name):
            errors.append("Skill name must use lowercase letters, digits, and hyphens only")
        elif name != root.name:
            warnings.append(f"Skill name {name!r} differs from folder name {root.name!r}")

        if not description:
            errors.append("SKILL.md frontmatter missing description")
        else:
            if not description.startswith("Use when"):
                errors.append("Description must start with 'Use when'")
            if len(description) > 500:
                errors.append("Description should stay under 500 characters")

        frontmatter_block = re.match(r"^---\n(.*?)\n---", text, flags=re.S)
        if frontmatter_block and len(frontmatter_block.group(1)) > 1024:
            errors.append("Frontmatter exceeds 1024 characters")

        for rel in REFERENCE_LINKS:
            if rel not in text:
                warnings.append(f"SKILL.md does not mention {rel}")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
    }


def print_text(result: dict) -> None:
    print(f"Skill self-check: {'OK' if result['ok'] else 'FAILED'}")
    if result["errors"]:
        print("\nErrors:")
        for item in result["errors"]:
            print(f"- {item}")
    if result["warnings"]:
        print("\nWarnings:")
        for item in result["warnings"]:
            print(f"- {item}")
    if not result["errors"] and not result["warnings"]:
        print("No errors or warnings.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_root", type=Path, help="Path to the skill folder")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    result = analyze(args.skill_root)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
