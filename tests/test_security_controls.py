import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cloudguard.deployment.gate import evaluate
from cloudguard.remediation.validator import repair_and_validate, scan


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

    def test_gate_allows_below_threshold(self):
        result = evaluate([{"policy_sid": "POL_AWS_RDS_ENCRYPTION", "severity": "MEDIUM"}], block_at="HIGH")
        self.assertEqual(result["decision"], "ALLOW")

    def test_gate_deduplicates_same_finding(self):
        finding = {"policy_sid": "POL_AWS_S3_PUBLIC", "severity": "CRITICAL", "file": "tf_001", "resource": "bucket"}
        result = evaluate([finding, dict(finding)])
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["blocking_count"], 1)

    def test_detector_covers_all_supported_policy_patterns(self):
        source = """
        acl = "public-read"
        publicly_accessible = true
        storage_encrypted = false
        cidr_blocks = ["0.0.0.0/0"]
        action = "*"
        """
        self.assertEqual(
            scan(source),
            {
                "POL_AWS_S3_PUBLIC",
                "POL_AWS_RDS_PUBLIC",
                "POL_AWS_RDS_ENCRYPTION",
                "POL_AWS_SG_UNRESTRICTED",
                "POL_AWS_IAM_WILDCARD",
            },
        )
