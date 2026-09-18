#!/usr/bin/env python3
"""Compute this project's Gate 1 mechanical trend metrics and append a progress-log row.

Implements the recording half of principles/progress-tracking.md Gate 1: "each execution
appends a row to the project's progress log capturing before/after values for each
metric... and pass/fail." This script computes the "after" values, diffs them against the
log's last row (the prior "after" = this run's "before"), prints a PASS/FAIL verdict, and
appends the new row.

Deliberately excludes actual test execution and coverage: those need a Godot install
(`dev_kit/ci/godot/scripts/run_tests.ps1`) and aren't reliably invokable from a plain
Python script across local/CI environments. Test *count* is a static grep instead; test
*coverage* stays the documented manual step until a confirmed GdUnit4 coverage CLI flag
exists (see dev_kit/ci/godot/README.md).
"""
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
LOG_PATH = REPO_ROOT / "dev_kit" / "progress-log.md"
SCRIPTS_DIR = Path(__file__).resolve().parent

STATIC_CHECKS = [
    ("srp-size", ["check_size_budgets.py"]),
    ("naming-grep-discoverable", ["check_naming.py"]),
    ("isp", ["check_isp.py"]),
    ("dip-direction", ["check_dip_direction.py"]),
    ("no-cross-cutting-helper-violation", ["check_helper_promotion.py"]),
]

COLUMNS = [
    "Date",
    "Ref",
    "Automated checks passing",
    "Test count",
    "Coverage",
    "Lint warnings",
    "Size violations",
    "Naming violations",
    "ISP violations",
    "DIP violations",
    "Helper violations",
    "Gate 1",
]

# Higher is worse for these columns (numeric ones only; "Automated checks passing" and
# "Test count" are the opposite - lower is worse).
WORSE_WHEN_HIGHER = {
    "Lint warnings",
    "Size violations",
    "Naming violations",
    "ISP violations",
    "DIP violations",
    "Helper violations",
}
WORSE_WHEN_LOWER = {"Automated checks passing", "Test count"}


def run_check(script_name: str) -> tuple[bool, int]:
    """Run a check script, return (passed, violation_count from '  - ' lines)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    violation_lines = [line for line in result.stdout.splitlines() if line.strip().startswith("- ")]
    return result.returncode == 0, len(violation_lines)


def count_lint_warnings() -> int:
    result = subprocess.run(
        ["gdlint", "src", "tests"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    match = re.search(r"Failure: (\d+) problems? found", result.stdout)
    if match:
        return int(match.group(1))
    return 0


def count_tests() -> int:
    tests_dir = REPO_ROOT / "tests"
    if not tests_dir.exists():
        return 0
    pattern = re.compile(r"^\s*func\s+test_\w+")
    return sum(
        1
        for gd_file in tests_dir.rglob("*.gd")
        for line in gd_file.read_text(encoding="utf-8").splitlines()
        if pattern.match(line)
    )


def gather_metrics() -> dict:
    violation_counts = {}
    passing = 0
    for label, script_args in STATIC_CHECKS:
        ok, count = run_check(script_args[0])
        violation_counts[label] = count
        if ok:
            passing += 1

    lint_warnings = count_lint_warnings()
    if lint_warnings == 0:
        passing += 1

    return {
        "Automated checks passing": f"{passing}/{len(STATIC_CHECKS) + 1}",
        "Test count": count_tests(),
        "Coverage": "manual (GdUnit4 editor inspector)",
        "Lint warnings": lint_warnings,
        "Size violations": violation_counts["srp-size"],
        "Naming violations": violation_counts["naming-grep-discoverable"],
        "ISP violations": violation_counts["isp"],
        "DIP violations": violation_counts["dip-direction"],
        "Helper violations": violation_counts["no-cross-cutting-helper-violation"],
    }


def parse_last_row() -> dict | None:
    if not LOG_PATH.exists():
        return None
    rows = [
        line
        for line in LOG_PATH.read_text(encoding="utf-8").splitlines()
        if line.startswith("|") and not line.startswith("|---") and "Date" not in line
    ]
    if not rows:
        return None
    cells = [cell.strip() for cell in rows[-1].strip("|").split("|")]
    return dict(zip(COLUMNS, cells))


def compare(previous: dict | None, current: dict) -> tuple[bool, list[str]]:
    if previous is None:
        return True, []

    regressions = []
    for column in WORSE_WHEN_HIGHER:
        try:
            if int(current[column]) > int(previous[column]):
                regressions.append(
                    f"{column} increased: {previous[column]} -> {current[column]}"
                )
        except (KeyError, ValueError):
            continue

    for column in WORSE_WHEN_LOWER:
        try:
            prev_val = previous[column].split("/")[0] if "/" in previous.get(column, "") else previous.get(column)
            curr_val = current[column].split("/")[0] if "/" in str(current.get(column, "")) else current.get(column)
            if int(curr_val) < int(prev_val):
                regressions.append(
                    f"{column} decreased: {previous[column]} -> {current[column]}"
                )
        except (KeyError, ValueError, TypeError):
            continue

    return len(regressions) == 0, regressions


def append_row(ref: str, metrics: dict, gate1_pass: bool) -> None:
    if not LOG_PATH.exists():
        header = "| " + " | ".join(COLUMNS) + " |\n"
        header += "|" + "|".join(["---"] * len(COLUMNS)) + "|\n"
        LOG_PATH.write_text(header, encoding="utf-8")

    row_values = [
        datetime.now(timezone.utc).date().isoformat(),
        ref,
        str(metrics["Automated checks passing"]),
        str(metrics["Test count"]),
        str(metrics["Coverage"]),
        str(metrics["Lint warnings"]),
        str(metrics["Size violations"]),
        str(metrics["Naming violations"]),
        str(metrics["ISP violations"]),
        str(metrics["DIP violations"]),
        str(metrics["Helper violations"]),
        "PASS" if gate1_pass else "FAIL",
    ]
    row = "| " + " | ".join(row_values) + " |\n"
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(row)


def main() -> int:
    ref = sys.argv[1] if len(sys.argv) > 1 else "unlabeled"
    previous = parse_last_row()
    current = gather_metrics()
    gate1_pass, regressions = compare(previous, current)

    append_row(ref, current, gate1_pass)

    print(f"Progress log row appended to {LOG_PATH.relative_to(REPO_ROOT)} for '{ref}'.")
    for key, value in current.items():
        print(f"  {key}: {value}")

    if not gate1_pass:
        print("\nGate 1 FAIL - regression(s) vs. previous row:")
        for regression in regressions:
            print(f"  - {regression}")
        return 1

    print("\nGate 1: no regression vs. previous row.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
