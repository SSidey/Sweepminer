#!/usr/bin/env python3
"""Fail if any .gd file/function exceeds the size budgets in config/thresholds.yaml.

Implements the `srp-size` row of rubrics/run-baseline.rubrics.md.
"""
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
THRESHOLDS_PATH = Path(__file__).resolve().parents[3] / "config" / "thresholds.yaml"
SCAN_DIRS = ("src", "tests")
FUNC_RE = re.compile(r"^(\s*)(?:static\s+)?func\s+\w+")


def load_thresholds() -> dict:
    with THRESHOLDS_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def function_line_counts(lines: list[str]) -> list[tuple[str, int]]:
    counts = []
    current_name = None
    current_indent = None
    current_len = 0
    for line in lines:
        match = FUNC_RE.match(line)
        if match:
            if current_name is not None:
                counts.append((current_name, current_len))
            current_indent = len(match.group(1))
            current_name = line.strip().split("(")[0]
            current_len = 1
            continue
        if current_name is not None:
            stripped = line.rstrip("\n")
            is_blank_or_deeper = (
                stripped.strip() == "" or len(line) - len(line.lstrip(" \t")) > current_indent
            )
            if is_blank_or_deeper:
                current_len += 1
            else:
                counts.append((current_name, current_len))
                current_name = None
    if current_name is not None:
        counts.append((current_name, current_len))
    return counts


def main() -> int:
    thresholds = load_thresholds()
    max_file_lines = thresholds["solid_mechanical"]["srp"]["max_file_lines"]
    max_function_lines = thresholds["solid_mechanical"]["srp"]["max_function_lines"]

    violations = []
    for scan_dir in SCAN_DIRS:
        for gd_file in (REPO_ROOT / scan_dir).rglob("*.gd") if (REPO_ROOT / scan_dir).exists() else []:
            lines = gd_file.read_text(encoding="utf-8").splitlines()
            if len(lines) > max_file_lines:
                violations.append(
                    f"{gd_file.relative_to(REPO_ROOT)}: {len(lines)} lines "
                    f"(budget: {max_file_lines})"
                )
            for name, length in function_line_counts(lines):
                if length > max_function_lines:
                    violations.append(
                        f"{gd_file.relative_to(REPO_ROOT)}: {name} is {length} lines "
                        f"(budget: {max_function_lines})"
                    )

    if violations:
        print("srp-size violations (see principles/decision-ledger.md to record an exception):")
        for violation in violations:
            print(f"  - {violation}")
        return 1

    print("srp-size: no violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
