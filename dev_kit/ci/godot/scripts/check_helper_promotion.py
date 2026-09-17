#!/usr/bin/env python3
"""Fail if a helper has been dumped into a generic catch-all file.

Implements the `no-cross-cutting-helper-violation` row of rubrics/run-baseline.rubrics.md
via the concrete, named failure mode principles/ai-first-organisation.md Principle 4
calls out explicitly: a promoted helper must go into a precisely named module, "never into
a generic utils.*, helpers.*, or common.* file."

Honest limit: this only catches the catch-all-filename shape of the violation. It cannot
detect a helper that's below the promotion threshold (used by <3 callers) but has already
been incorrectly promoted into its own file, nor a genuinely shared helper duplicated
past the threshold instead of promoted - both require call-graph analysis this project
doesn't have yet.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SCAN_DIRS = ("src", "tests")
FORBIDDEN_STEMS = {"utils", "helpers", "helper", "common", "base", "manager"}


def main() -> int:
    violations = []
    for scan_dir in SCAN_DIRS:
        directory = REPO_ROOT / scan_dir
        if not directory.exists():
            continue
        for gd_file in directory.rglob("*.gd"):
            if gd_file.stem.lower() in FORBIDDEN_STEMS:
                violations.append(str(gd_file.relative_to(REPO_ROOT)))

    if violations:
        print(
            "no-cross-cutting-helper-violation: generic catch-all filename(s) found "
            "(rename to what the module actually does):"
        )
        for violation in violations:
            print(f"  - {violation}")
        return 1

    print("no-cross-cutting-helper-violation: no violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
