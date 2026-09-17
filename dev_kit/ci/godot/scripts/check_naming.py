#!/usr/bin/env python3
"""Fail if any identifier defined under src/ has too many grep hits across the codebase.

Implements the `naming-grep-discoverable` row of rubrics/run-baseline.rubrics.md. This
checks the mechanical hit-count test only; the judgement of whether a name is
legitimately scoped (e.g. a `process` method on a single class) per
principles/ai-first-organisation.md Principle 3 stays a manual review.
"""
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
THRESHOLDS_PATH = Path(__file__).resolve().parents[3] / "config" / "thresholds.yaml"
SCAN_DIRS = ("src", "tests")
DEFINITION_RE = re.compile(
    r"^\s*(?:class_name|const|(?:static\s+)?func|class)\s+(\w+)"
)


def load_thresholds() -> dict:
    with THRESHOLDS_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def gather_source_files() -> list[Path]:
    files = []
    for scan_dir in SCAN_DIRS:
        directory = REPO_ROOT / scan_dir
        if directory.exists():
            files.extend(directory.rglob("*.gd"))
    return files


def gather_identifiers(files: list[Path]) -> set[str]:
    identifiers = set()
    for gd_file in files:
        for line in gd_file.read_text(encoding="utf-8").splitlines():
            match = DEFINITION_RE.match(line)
            if match:
                identifiers.add(match.group(1))
    return identifiers


def count_hits(identifier: str, files: list[Path]) -> int:
    pattern = re.compile(rf"\b{re.escape(identifier)}\b")
    return sum(
        len(pattern.findall(gd_file.read_text(encoding="utf-8"))) for gd_file in files
    )


def main() -> int:
    thresholds = load_thresholds()
    max_grep_hits = thresholds["ai_first_organisation"]["naming"]["max_grep_hits"]

    files = gather_source_files()
    identifiers = gather_identifiers(files)

    violations = []
    for identifier in sorted(identifiers):
        hits = count_hits(identifier, files)
        if hits >= max_grep_hits:
            violations.append(f"{identifier}: {hits} hits (threshold: {max_grep_hits})")

    if violations:
        print("naming-grep-discoverable violations (rename, or scope+justify per Principle 3):")
        for violation in violations:
            print(f"  - {violation}")
        return 1

    print("naming-grep-discoverable: no violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
