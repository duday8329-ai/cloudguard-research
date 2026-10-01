"""Create the versioned 12-manifest CloudGuard sanity benchmark.

The files are intentionally small, synthetic, and labelled by the project team.
They test the data and metric pipeline; they are not a conference-scale corpus.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("tf_001", "terraform", "aws_s3_bucket.data", "POL_AWS_S3_PUBLIC", 1, "CRITICAL", 'resource "aws_s3_bucket" "data" { bucket = "demo-public" acl = "public-read" }'),
    ("tf_002", "terraform", "aws_s3_bucket.logs", "POL_AWS_S3_PUBLIC", 0, "CRITICAL", 'resource "aws_s3_bucket" "logs" { bucket = "demo-private" acl = "private" }'),
    ("tf_003", "terraform", "aws_db_instance.customer", "POL_AWS_RDS_PUBLIC", 1, "CRITICAL", 'resource "aws_db_instance" "customer" { publicly_accessible = true storage_encrypted = true }'),
    ("tf_004", "terraform", "aws_db_instance.customer", "POL_AWS_RDS_ENCRYPTION", 0, "HIGH", 'resource "aws_db_instance" "customer" { publicly_accessible = false storage_encrypted = true }'),
    ("tf_005", "terraform", "aws_security_group.web", "POL_AWS_SG_UNRESTRICTED", 1, "HIGH", 'resource "aws_security_group" "web" { ingress { from_port = 22 to_port = 22 cidr_blocks = ["0.0.0.0/0"] } }'),
    ("tf_006", "terraform", "aws_security_group.web", "POL_AWS_SG_UNRESTRICTED", 0, "HIGH", 'resource "aws_security_group" "web" { ingress { from_port = 443 to_port = 443 cidr_blocks = ["10.0.0.0/8"] } }'),
    ("cf_001", "cloudformation", "AppPolicy", "POL_AWS_IAM_WILDCARD", 1, "HIGH", 'Resources:\n  AppPolicy:\n    Type: AWS::IAM::Policy\n    Properties:\n      PolicyDocument: {"Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}]}'),
    ("cf_002", "cloudformation", "AppPolicy", "POL_AWS_IAM_WILDCARD", 0, "HIGH", 'Resources:\n  AppPolicy:\n    Type: AWS::IAM::Policy\n    Properties:\n      PolicyDocument: {"Statement": [{"Effect": "Allow", "Action": "s3:GetObject", "Resource": "*"}]}'),
    ("cf_003", "cloudformation", "PrimaryDb", "POL_AWS_RDS_ENCRYPTION", 1, "HIGH", 'Resources:\n  PrimaryDb:\n    Type: AWS::RDS::DBInstance\n    Properties:\n      PubliclyAccessible: false\n      StorageEncrypted: false'),
    ("cf_004", "cloudformation", "PrimaryDb", "POL_AWS_RDS_PUBLIC", 0, "CRITICAL", 'Resources:\n  PrimaryDb:\n    Type: AWS::RDS::DBInstance\n    Properties:\n      PubliclyAccessible: false\n      StorageEncrypted: true'),
    ("cf_005", "cloudformation", "Artifacts", "POL_AWS_S3_PUBLIC", 1, "CRITICAL", 'Resources:\n  Artifacts:\n    Type: AWS::S3::Bucket\n    Properties:\n      AccessControl: PublicRead'),
    ("cf_006", "cloudformation", "Artifacts", "POL_AWS_S3_PUBLIC", 0, "CRITICAL", 'Resources:\n  Artifacts:\n    Type: AWS::S3::Bucket\n    Properties:\n      AccessControl: Private'),
]

# Each RDS configuration is evaluated for both public exposure and encryption.
# These additional rows share an existing source manifest rather than creating
# another file, which is precisely the point of policy-instance labelling.
EXTRA_RDS_LABELS = [
    ("tf_003", "terraform", "aws_db_instance.customer", "POL_AWS_RDS_ENCRYPTION", 0, "HIGH"),
    ("tf_004", "terraform", "aws_db_instance.customer", "POL_AWS_RDS_PUBLIC", 0, "CRITICAL"),
    ("cf_003", "cloudformation", "PrimaryDb", "POL_AWS_RDS_PUBLIC", 0, "CRITICAL"),
    ("cf_004", "cloudformation", "PrimaryDb", "POL_AWS_RDS_ENCRYPTION", 0, "HIGH"),
]


def write_csv(path: Path, headers: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    manifest, labels = [], []
    for file_id, fmt, resource_id, sid, violation, severity, content in CASES:
        suffix = ".tf" if fmt == "terraform" else ".yaml"
        target = ROOT / "benchmark" / fmt / file_id / f"main{suffix}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content + "\n", encoding="utf-8")
        manifest.append({"file_id": file_id, "format": fmt, "path": str(target.relative_to(ROOT)).replace("\\", "/")})
        labels.append({"instance_id": f"U_{file_id}", "file_id": file_id, "format": fmt, "resource_id": resource_id, "policy_sid": sid, "expected_violation": violation, "severity": severity, "annotation_source": "project_team"})
    for file_id, fmt, resource_id, sid, violation, severity in EXTRA_RDS_LABELS:
        labels.append({"instance_id": f"U_{file_id}_{sid}", "file_id": file_id, "format": fmt, "resource_id": resource_id, "policy_sid": sid, "expected_violation": violation, "severity": severity, "annotation_source": "project_team"})
    write_csv(ROOT / "benchmark" / "benchmark_manifest.csv", ["file_id", "format", "path"], manifest)
    fields = ["instance_id", "file_id", "format", "resource_id", "policy_sid", "expected_violation", "severity", "annotation_source"]
    write_csv(ROOT / "annotations" / "consensus.csv", fields, labels)
    print(f"Created {len(manifest)} manifests and {len(labels)} policy-instance labels.")


if __name__ == "__main__":
    main()
