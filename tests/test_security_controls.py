import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cloudguard.deployment.gate import evaluate
from cloudguard.remediation.validator import repair_and_validate


class SecurityControlTests(unittest.TestCase):
    def test_safe_repairs_clear_findings(self):
        source = 'resource "aws_db_instance" "db" {\n publicly_accessible = true\n storage_encrypted = false\n}\n'
        result = repair_and_validate(source, ["POL_AWS_RDS_PUBLIC", "POL_AWS_RDS_ENCRYPTION"])
        self.assertEqual(result["after"], [])
        self.assertTrue(all(case["cleared"] for case in result["cases"]))

    def test_sensitive_repairs_require_approval(self):
        result = repair_and_validate('cidr_blocks = ["0.0.0.0/0"]', ["POL_AWS_SG_UNRESTRICTED"])
        self.assertEqual(result["after"], ["POL_AWS_SG_UNRESTRICTED"])
        self.assertFalse(result["cases"][0]["auto_fixable"])

    def test_gate_blocks_high(self):
        result = evaluate([{"policy_sid": "POL_AWS_RDS_PUBLIC", "severity": "CRITICAL"}])
        self.assertEqual(result["decision"], "BLOCK")
