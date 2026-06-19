import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = SKILL_ROOT / "scripts" / "skill_self_check.py"


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
