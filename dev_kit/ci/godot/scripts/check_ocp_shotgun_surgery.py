#!/usr/bin/env python3
"""Fail if this diff modifies too many pre-existing files under src/.

Implements the `ocp-shotgun-surgery` row of rubrics/run-baseline.rubrics.md: adding one
new case/behaviour should plug into an existing extension point, not require editing many
already-shipped files.

Honest limit (per principles/solid-mechanical.md's own convention): this counts
*modified* pre-existing files under src/ against the base ref - it cannot distinguish
"one new case forced N files open" from any other reason N files changed together (e.g. a
deliberate, justified refactor). A genuine exception should be recorded as a Decision
(dev_kit/principles/decision-ledger.md), not silently ignored.
"""
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
THRESHOLDS_PATH = Path(__file__).resolve().parents[3] / "config" / "thresholds.yaml"
SCAN_PREFIX = "src/"


def load_thresholds() -> dict:
    with THRESHOLDS_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def modified_preexisting_files(base_ref: str) -> list[str]:
    merge_base = subprocess.run(
        ["git", "merge-base", base_ref, "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    diff = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=M", merge_base, "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()

    return [path for path in diff if path.startswith(SCAN_PREFIX)]


def main() -> int:
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    thresholds = load_thresholds()
    max_touched = thresholds["solid_mechanical"]["ocp"]["max_touched_files_per_new_case"]

    try:
        touched = modified_preexisting_files(base_ref)
    except subprocess.CalledProcessError as error:
        print(f"ocp-shotgun-surgery: could not diff against '{base_ref}': {error}")
        return 0

    if len(touched) >= max_touched:
        print(
            f"ocp-shotgun-surgery: {len(touched)} pre-existing src/ files modified "
            f"(threshold: {max_touched}). If this is one new case/behaviour, it should "
            f"plug into an existing extension point instead. If it's a justified "
            f"broad change, record why in a Decision "
            f"(dev_kit/principles/decision-ledger.md):"
        )
        for path in touched:
            print(f"  - {path}")
        return 1

    print(f"ocp-shotgun-surgery: {len(touched)} pre-existing src/ files modified, below threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
