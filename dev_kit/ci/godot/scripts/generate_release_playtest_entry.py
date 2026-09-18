#!/usr/bin/env python3
"""Append a new versioned PLAYTEST_LOG.md entry, pre-filled with the mechanical Release
Readiness Score and blank fields for the player to fill in.

Run by .github/workflows/release.yml once determine_version_bump.py finds a warranted
bump. See Decision 5 in sweepminer-spec-v0.3.md for what this score does and doesn't mean,
and PLAYTEST_LOG.md itself for how to fill in an entry after playing.
"""
import argparse
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import release_score  # noqa: E402
from report_progress import parse_last_row  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAYTEST_LOG_PATH = REPO_ROOT / "PLAYTEST_LOG.md"
VERSION_PATH = REPO_ROOT / "VERSION"

ENTRY_TEMPLATE = """
### v{version} — {date}

**Mechanical (Release Readiness Score): {score}/100**
- Automated checks: {automated_checks} ({automated_checks_component}/60)
- Tests: {test_note} ({test_component}/40)
- Full metrics: see `dev_kit/progress-log.md`, ref `{ref}`

**Functional rating (1-5):** _fill in after playtesting_
**Fun/engagement rating (1-5):** _fill in after playtesting_

**Bug entries:**

| Severity | What happened | Repro steps |
|---|---|---|
| _blocker / major / minor_ | | |

**Session/completion notes:** _fill in after playtesting_
"""


def parse_junit_pass_ratio(report_path: Path | None) -> float | None:
    if report_path is None or not report_path.exists():
        return None

    total = failures = errors = 0
    tree = ET.parse(report_path)
    for testsuite in tree.getroot().iter("testsuite"):
        total += int(testsuite.get("tests", 0))
        failures += int(testsuite.get("failures", 0))
        errors += int(testsuite.get("errors", 0))

    if total == 0:
        return None
    return (total - failures - errors) / total


def parse_automated_checks_ratio(row: dict) -> float:
    passing, out_of = row["Automated checks passing"].split("/")
    return int(passing) / int(out_of)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="New version, e.g. v0.1.0")
    parser.add_argument("--junit-report", type=Path, default=None)
    args = parser.parse_args()

    row = parse_last_row()
    if row is None:
        print(
            "No dev_kit/progress-log.md row found - run report_progress.py first.",
            file=sys.stderr,
        )
        return 1

    automated_ratio = parse_automated_checks_ratio(row)
    test_ratio = parse_junit_pass_ratio(args.junit_report)
    scoring = release_score.compute_score(automated_ratio, test_ratio)

    entry = ENTRY_TEMPLATE.format(
        version=args.version.lstrip("v"),
        date=datetime.now(timezone.utc).date().isoformat(),
        score=scoring["score"],
        automated_checks=row["Automated checks passing"],
        automated_checks_component=scoring["automated_checks_component"],
        test_note=scoring["test_note"],
        test_component=scoring["test_component"],
        ref=row["Ref"],
    )

    with PLAYTEST_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(entry)

    VERSION_PATH.write_text(args.version.lstrip("v") + "\n", encoding="utf-8")

    print(f"Appended PLAYTEST_LOG.md entry for {args.version} - score {scoring['score']}/100.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
