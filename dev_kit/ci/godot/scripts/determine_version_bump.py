#!/usr/bin/env python3
"""Decide whether the commits since the last release tag warrant a version bump.

Implements the versioning scheme in Decision 5 of sweepminer-spec-v0.3.md: semantic
version tags computed from Conventional Commits since the last `vX.Y.Z` tag. Prints
`BUMP=<new-version-or-none>`, `PREVIOUS=<prior-tag-or-none>`, and `LEVEL=<major|minor|
patch|none>` as `KEY=value` lines (suitable for `>> $GITHUB_OUTPUT`), and exits 0 if a
bump is warranted, 1 if not.

Pre-1.0 exception (see Decision 5): while MAJOR is 0, a breaking change bumps MINOR, not
MAJOR - semver's own "initial development" convention.
"""
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
TYPE_RE = re.compile(r"^(\w+)(\([\w./-]+\))?(!)?:")
BREAKING_FOOTER_RE = re.compile(r"^BREAKING CHANGE:", re.MULTILINE)

RANK = {"patch": 0, "minor": 1, "major": 2}
RECORD_SEP = "\x1e"
UNIT_SEP = "\x1f"


def latest_tag() -> str | None:
    result = subprocess.run(
        ["git", "tag", "--list", "v*.*.*", "--sort=-v:refname"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    for line in result.stdout.splitlines():
        if TAG_RE.match(line.strip()):
            return line.strip()
    return None


def commits_since(tag: str | None) -> list[tuple[str, str]]:
    range_arg = f"{tag}..HEAD" if tag else "HEAD"
    result = subprocess.run(
        ["git", "log", range_arg, f"--pretty=format:%s{UNIT_SEP}%b{RECORD_SEP}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    commits = []
    for chunk in result.stdout.split(RECORD_SEP):
        if not chunk.strip():
            continue
        subject, _, body = chunk.partition(UNIT_SEP)
        commits.append((subject.strip(), body.strip()))
    return commits


def classify(commits: list[tuple[str, str]]) -> str | None:
    highest = None
    for subject, body in commits:
        match = TYPE_RE.match(subject)
        if not match:
            continue
        commit_type = match.group(1)
        is_breaking = bool(match.group(3)) or bool(BREAKING_FOOTER_RE.search(body))

        if is_breaking:
            level = "major"
        elif commit_type == "feat":
            level = "minor"
        elif commit_type == "fix":
            level = "patch"
        else:
            continue

        if highest is None or RANK[level] > RANK[highest]:
            highest = level
    return highest


def bump_version(tag: str | None, level: str) -> str:
    if tag is None:
        major, minor, patch = 0, 0, 0
    else:
        match = TAG_RE.match(tag)
        major, minor, patch = (int(part) for part in match.groups())

    if major == 0 and level == "major":
        level = "minor"  # pre-1.0 exception, see Decision 5

    if level == "major":
        return f"v{major + 1}.0.0"
    if level == "minor":
        return f"v{major}.{minor + 1}.0"
    return f"v{major}.{minor}.{patch + 1}"


def main() -> int:
    tag = latest_tag()
    commits = commits_since(tag)
    level = classify(commits)

    print(f"PREVIOUS={tag or 'none'}")
    print(f"LEVEL={level or 'none'}")

    if level is None:
        print("BUMP=none")
        return 1

    print(f"BUMP={bump_version(tag, level)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
