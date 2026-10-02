from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cloudguard.remediation.validator import repair_and_validate


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair supported CloudGuard findings and re-scan the result.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--sid", action="append", required=True)
    parser.add_argument("--approved-cidr")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = repair_and_validate(args.source.read_text(encoding="utf-8"), args.sid, args.approved_cidr)
    if args.output:
        args.output.write_text(result["source"], encoding="utf-8")
    print({k: result[k] for k in ("before", "after", "structural_check", "cases")})
    return 0 if result["structural_check"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
