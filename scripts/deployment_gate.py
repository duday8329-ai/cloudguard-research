from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cloudguard.deployment.gate import evaluate


def main() -> int:
    parser = argparse.ArgumentParser(description="Return a CI-friendly ALLOW/BLOCK decision.")
    parser.add_argument("findings", type=Path, help="JSON array of findings")
    parser.add_argument("--block-at", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"], default="HIGH")
    parser.add_argument("--require-clean-repair", action="store_true")
    args = parser.parse_args()
    findings = json.loads(args.findings.read_text(encoding="utf-8"))
    result = evaluate(findings, args.block_at, args.require_clean_repair)
    print(json.dumps(result, indent=2))
    return 1 if result["decision"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
