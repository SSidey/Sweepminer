#!/usr/bin/env python3
"""Fail if domain logic under src/ depends on low-level/engine or scene infrastructure.

Implements the `dip-direction` row of rubrics/run-baseline.rubrics.md, using this
project's own directory convention as the domain/infrastructure boundary: `src/` is
engine-agnostic game logic, `scenes/` is Godot node/scene glue. That boundary didn't
formally exist when dev_kit/ci/godot/README.md was first written (hence "judgement-only
until that separation exists") - it now does, so this check enforces it:

1. A `src/**/*.gd` file must not `extends` a Godot engine Node-derived class - only
   `RefCounted`, `Resource`, `Object`, or another `src/`-defined class.
2. A `src/**/*.gd` file must not `preload`/`load` anything under `res://scenes/`.

Honest limit: this is a directory-and-keyword heuristic, not a full call-graph analysis
(rubrics/run-baseline.rubrics.md's own stated tool for this row). It catches the two
concrete violation shapes above; it doesn't catch every possible dependency-direction
mistake (e.g. a domain file passing a Node instance around after receiving it as an
argument is invisible to this static scan).
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SRC_DIR = REPO_ROOT / "src"

EXTENDS_RE = re.compile(r"^extends\s+(\w+)")
CLASS_NAME_RE = re.compile(r"^class_name\s+(\w+)")
SCENE_LOAD_RE = re.compile(r"(?:preload|load)\(\s*[\"']res://scenes/")

DOMAIN_SAFE_BASE_TYPES = {"RefCounted", "Resource", "Object"}


def gather_domain_class_names() -> set[str]:
    names = set()
    for gd_file in SRC_DIR.rglob("*.gd"):
        for line in gd_file.read_text(encoding="utf-8").splitlines():
            match = CLASS_NAME_RE.match(line)
            if match:
                names.add(match.group(1))
    return names


def main() -> int:
    if not SRC_DIR.exists():
        print("dip-direction: no src/ directory yet, nothing to check.")
        return 0

    domain_class_names = gather_domain_class_names()
    allowed_base_types = DOMAIN_SAFE_BASE_TYPES | domain_class_names

    violations = []
    for gd_file in SRC_DIR.rglob("*.gd"):
        rel_path = gd_file.relative_to(REPO_ROOT)
        lines = gd_file.read_text(encoding="utf-8").splitlines()

        for line in lines:
            extends_match = EXTENDS_RE.match(line)
            if extends_match and extends_match.group(1) not in allowed_base_types:
                violations.append(
                    f"{rel_path}: extends '{extends_match.group(1)}' - domain logic "
                    f"under src/ should only extend RefCounted/Resource/Object or "
                    f"another src/ class, not an engine Node type"
                )

            if SCENE_LOAD_RE.search(line):
                violations.append(
                    f"{rel_path}: loads a scene from res://scenes/ - domain logic "
                    f"under src/ must not depend on scene/UI infrastructure"
                )

    if violations:
        print("dip-direction violations:")
        for violation in violations:
            print(f"  - {violation}")
        return 1

    print("dip-direction: no violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
