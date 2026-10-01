"""Build a 50-manifest synthetic mutation benchmark for CloudGuard.

All configurations are intentionally generated project-team test cases, not
enterprise artefacts or independently annotated data. Every source and label is
recreated deterministically by this file.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICIES = [
    ("s3", "POL_AWS_S3_PUBLIC", "CRITICAL"),
    ("rds_public", "POL_AWS_RDS_PUBLIC", "CRITICAL"),
    ("rds_encryption", "POL_AWS_RDS_ENCRYPTION", "HIGH"),
    ("sg", "POL_AWS_SG_UNRESTRICTED", "HIGH"),
    ("iam", "POL_AWS_IAM_WILDCARD", "HIGH"),
]


def terraform(kind: str, name: str, vulnerable: bool) -> tuple[str, str]:
    if kind == "s3":
        acl = "public-read" if vulnerable else "private"
        return f"aws_s3_bucket.{name}", f'resource "aws_s3_bucket" "{name}" {{\n  bucket = "cloudguard-{name}"\n  acl = "{acl}"\n}}\n'
    if kind.startswith("rds"):
        public = vulnerable if kind == "rds_public" else False
        encrypted = False if kind == "rds_encryption" and vulnerable else True
        return f"aws_db_instance.{name}", f'resource "aws_db_instance" "{name}" {{\n  allocated_storage = 20\n  engine = "postgres"\n  instance_class = "db.t3.micro"\n  username = "admin"\n  password = "change-me-for-test-only"\n  skip_final_snapshot = true\n  publicly_accessible = {str(public).lower()}\n  storage_encrypted = {str(encrypted).lower()}\n}}\n'
    if kind == "sg":
        cidr = "0.0.0.0/0" if vulnerable else "10.0.0.0/8"
        return f"aws_security_group.{name}", f'resource "aws_security_group" "{name}" {{\n  name = "{name}"\n  ingress {{\n    from_port = 22\n    to_port = 22\n    protocol = "tcp"\n    cidr_blocks = ["{cidr}"]\n  }}\n}}\n'
    action = "*" if vulnerable else "s3:GetObject"
    return f"aws_iam_policy.{name}", f'resource "aws_iam_policy" "{name}" {{\n  name = "{name}"\n  policy = jsonencode({{\n    Version = "2012-10-17"\n    Statement = [{{Effect = "Allow", Action = "{action}", Resource = "*"}}]\n  }})\n}}\n'


def cloudformation(kind: str, name: str, vulnerable: bool) -> tuple[str, str]:
    if kind == "s3":
        body = f"Type: AWS::S3::Bucket\n    Properties:\n      AccessControl: {'PublicRead' if vulnerable else 'Private'}"
    elif kind.startswith("rds"):
        public = vulnerable if kind == "rds_public" else False
        encrypted = False if kind == "rds_encryption" and vulnerable else True
        body = f"Type: AWS::RDS::DBInstance\n    Properties:\n      AllocatedStorage: 20\n      DBInstanceClass: db.t3.micro\n      Engine: postgres\n      MasterUsername: admin\n      MasterUserPassword: change-me-for-test-only\n      PubliclyAccessible: {str(public).lower()}\n      StorageEncrypted: {str(encrypted).lower()}"
    elif kind == "sg":
        cidr = "0.0.0.0/0" if vulnerable else "10.0.0.0/8"
        body = f"Type: AWS::EC2::SecurityGroup\n    Properties:\n      GroupDescription: CloudGuard test\n      SecurityGroupIngress:\n        - IpProtocol: tcp\n          FromPort: 22\n          ToPort: 22\n          CidrIp: {cidr}"
    else:
        action = "'*'" if vulnerable else "s3:GetObject"
        body = f"Type: AWS::IAM::ManagedPolicy\n    Properties:\n      ManagedPolicyName: {name}\n      PolicyDocument:\n        Version: '2012-10-17'\n        Statement:\n          - Effect: Allow\n            Action: {action}\n            Resource: '*'"
    return name, f"AWSTemplateFormatVersion: '2010-09-09'\nResources:\n  {name}:\n    {body}\n"


def write_csv(path: Path, headers: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    manifest: list[dict[str, object]] = []
    labels: list[dict[str, object]] = []
    for fmt in ("terraform", "cloudformation"):
        for policy_index, (kind, sid, severity) in enumerate(POLICIES, start=1):
            for variant in range(1, 6):
                vulnerable = variant <= 3
                file_no = (policy_index - 1) * 5 + variant
                file_id = f"{'tf' if fmt == 'terraform' else 'cf'}_{file_no:03}"
                logical_name = f"{kind.replace('_', '')}{variant}"
                creator = terraform if fmt == "terraform" else cloudformation
                resource_id, content = creator(kind, logical_name, vulnerable)
                suffix = ".tf" if fmt == "terraform" else ".yaml"
                target = ROOT / "benchmark" / fmt / file_id / f"main{suffix}"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                manifest.append({"file_id": file_id, "format": fmt, "path": str(target.relative_to(ROOT)).replace("\\", "/"), "provenance": "project_team_synthetic_mutation", "policy_family": sid})
                labels.append({"instance_id": f"U_{file_id}_{sid}", "file_id": file_id, "format": fmt, "resource_id": resource_id, "policy_sid": sid, "expected_violation": int(vulnerable), "severity": severity, "annotation_source": "project_team_predefined_policy_criteria"})
                if kind.startswith("rds"):
                    other_sid = "POL_AWS_RDS_ENCRYPTION" if sid == "POL_AWS_RDS_PUBLIC" else "POL_AWS_RDS_PUBLIC"
                    other_severity = "HIGH" if other_sid.endswith("ENCRYPTION") else "CRITICAL"
                    labels.append({"instance_id": f"U_{file_id}_{other_sid}", "file_id": file_id, "format": fmt, "resource_id": resource_id, "policy_sid": other_sid, "expected_violation": 0, "severity": other_severity, "annotation_source": "project_team_predefined_policy_criteria"})
    write_csv(ROOT / "benchmark" / "benchmark_manifest.csv", ["file_id", "format", "path", "provenance", "policy_family"], manifest)
    fields = ["instance_id", "file_id", "format", "resource_id", "policy_sid", "expected_violation", "severity", "annotation_source"]
    write_csv(ROOT / "annotations" / "consensus.csv", fields, labels)
    print(f"Created {len(manifest)} manifests and {len(labels)} policy-instance labels.")


if __name__ == "__main__":
    main()
