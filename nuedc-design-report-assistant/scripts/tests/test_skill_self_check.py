import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_ROOT / "scripts" / "skill_self_check.py"
EXCELLENT_REPORT_REF = "references/excellent-report-patterns.md"
AWARD_LEVEL_REF = "references/award-level-workflow.md"


class SkillSelfCheckTests(unittest.TestCase):
    def test_current_skill_passes_self_check(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(SKILL_ROOT), "--format", "json"],
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        output = json.loads(result.stdout)
        self.assertTrue(output["ok"])
        self.assertEqual(output["errors"], [])

    def test_excellent_report_patterns_are_bundled_and_routed(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        ref = SKILL_ROOT / EXCELLENT_REPORT_REF

        self.assertIn(EXCELLENT_REPORT_REF, skill_text)
        self.assertTrue(ref.is_file())

        ref_text = ref.read_text(encoding="utf-8")
        for phrase in (
            "优秀报告",
            "指标-设计-计算-测试-结论",
            "模块设计卡",
            "测试证据矩阵",
            "禁止复制",
        ):
            self.assertIn(phrase, ref_text)

    def test_award_level_full_workflow_is_bundled_and_routed(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        ref = SKILL_ROOT / AWARD_LEVEL_REF

        self.assertIn(AWARD_LEVEL_REF, skill_text)
        self.assertTrue(ref.is_file())

        ref_text = ref.read_text(encoding="utf-8")
        for phrase in (
            "省级一等奖",
            "赛题拆解",
            "方案论证",
            "分阶段调试",
            "端到端验证",
            "指标-方案-模块-调试-测试-报告",
        ):
            self.assertIn(phrase, ref_text)

    def test_self_check_requires_excellent_report_reference(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("skill_self_check", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)

        self.assertIn(EXCELLENT_REPORT_REF, module.REQUIRED_FILES)
        self.assertIn(EXCELLENT_REPORT_REF, module.REFERENCE_LINKS)
        self.assertIn(AWARD_LEVEL_REF, module.REQUIRED_FILES)
        self.assertIn(AWARD_LEVEL_REF, module.REFERENCE_LINKS)

    def test_current_markdown_files_do_not_contain_common_mojibake_tokens(self):
        mojibake_tokens = tuple(
            "".join(chr(codepoint) for codepoint in token)
            for token in (
                (0x934F, 0x310F, 0x6D97),
                (0x74A7, 0x6D98, 0x589F),
                (0x938A, 0x619F),
                (0x5BF0, 0x544D, 0xFF5E),
                (0x675E, 0xFE48, 0x6B22),
            )
        )
        offenders = []
        for path in SKILL_ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}:
                text = path.read_text(encoding="utf-8")
                for token in mojibake_tokens:
                    if token in text:
                        offenders.append(f"{path.relative_to(SKILL_ROOT).as_posix()} contains {token}")
                        break

        self.assertEqual(offenders, [])

    def test_missing_required_files_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "bad-skill"
            root.mkdir()
            (root / "SKILL.md").write_text(
                "---\nname: bad-skill\ndescription: Broken\n---\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--format", "json"],
                text=True,
                capture_output=True,
            )

        self.assertNotEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        self.assertFalse(output["ok"])
        self.assertTrue(any("agents/openai.yaml" in item for item in output["errors"]))


if __name__ == "__main__":
    unittest.main()
