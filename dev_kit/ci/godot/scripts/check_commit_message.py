#!/usr/bin/env python3
"""Fail if the commit message doesn't conform to Conventional Commits.

Implements the format half of the `commit-message-conforms` row in
rubrics/run-baseline.rubrics.md (templates/commit-message.md). This checks structure
only — whether the declared `type` actually matches the diff is a judgement call left
to review, per that template's own note.
"""
import re
import sys

TYPE_RE = re.compile(
    r"^(feat|fix|refactor|test|docs|chore|perf)(\([\w./-]+\))?!?: .{1,}"
)


def main() -> int:
    message_path = sys.argv[1]
    with open(message_path, encoding="utf-8") as handle:
        first_line = handle.readline().rstrip("\n")

    if not TYPE_RE.match(first_line):
        print(
            "commit-message-conforms: subject line must match "
            "'<type>[optional scope]: <description>' with type in "
            "feat|fix|refactor|test|docs|chore|perf (see templates/commit-message.md).\n"
            f"Got: {first_line!r}"
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
