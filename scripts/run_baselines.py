"""Record baseline runs without silently fabricating unavailable-tool output."""
from __future__ import annotations

import shutil
import sys


def main() -> None:
    missing = [name for name in ("checkov", "kics", "trivy") if shutil.which(name) is None]
    if missing:
        raise SystemExit(
            "Cannot produce comparison results. Install and version-pin these tools first: "
            + ", ".join(missing)
        )
    print("Baseline commands are available. Add frozen commands and output normalization before running a comparison.")


if __name__ == "__main__":
    main()
