from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class RepairResult:
    source: str
    policy_sid: str
    changed: bool
    auto_fixable: bool
    message: str


def repair(source: str, policy_sid: str, approved_cidr: str | None = None) -> RepairResult:
    """Apply only deterministic, reviewable fixes. Never invent access values."""
    if policy_sid == "POL_AWS_S3_PUBLIC":
        updated = re.sub(r'(?m)^([ \t]*acl[ \t]*=[ \t]*)["\'](?:public-read|public-write)["\']', r'\1"private"', source)
        if updated == source and re.search(r"public-read|public-write|publicread", source, re.I):
            updated = source + '\n\nresource "aws_s3_bucket_public_access_block" "cloudguard" {\n  bucket = aws_s3_bucket.project_files.id\n  block_public_acls = true\n  block_public_policy = true\n  ignore_public_acls = true\n  restrict_public_buckets = true\n}\n'
        return RepairResult(updated, policy_sid, updated != source, True, "Removed public S3 access and added a public-access block when needed.")
    if policy_sid == "POL_AWS_RDS_PUBLIC":
        updated = re.sub(r'(?im)^([ \t]*publicly_accessible[ \t]*[:=][ \t]*)(true)([ \t,}]*)', r'\1false\3', source)
        return RepairResult(updated, policy_sid, updated != source, True, "Set database public access to false.")
    if policy_sid == "POL_AWS_RDS_ENCRYPTION":
        updated = re.sub(r'(?im)^([ \t]*storage_encrypted[ \t]*[:=][ \t]*)(false)([ \t,}]*)', r'\1true\3', source)
        return RepairResult(updated, policy_sid, updated != source, True, "Enabled database storage encryption.")
    if policy_sid == "POL_AWS_SG_UNRESTRICTED":
        if not approved_cidr:
            return RepairResult(source, policy_sid, False, False, "Manual review required: an approved CIDR or security-group reference was not supplied.")
        updated = source.replace("0.0.0.0/0", approved_cidr)
        return RepairResult(updated, policy_sid, updated != source, True, f"Replaced unrestricted ingress with approved CIDR {approved_cidr}.")
    return RepairResult(source, policy_sid, False, False, "Manual review required: least-privilege intent cannot be inferred safely.")


def repair_all(source: str, policy_sids: list[str], approved_cidr: str | None = None) -> list[RepairResult]:
    results = []
    current = source
    for sid in policy_sids:
        result = repair(current, sid, approved_cidr)
        current = result.source
        results.append(result)
    return results
