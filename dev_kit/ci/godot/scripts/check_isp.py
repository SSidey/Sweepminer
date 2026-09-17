#!/usr/bin/env python3
"""Fail on ISP violations: fat classes (too many methods) and stub method bodies.

Implements the `isp-method-count` and `isp-stub-detection` rows of
rubrics/run-baseline.rubrics.md. Each GDScript file is treated as one class (GDScript's
natural unit), matching this project's one-concern-per-file convention.

Honest limits (per principles/solid-mechanical.md's own convention of stating what a
check does not prove): stub-detection here flags any trivial function body, not only
overrides of a base method with real behaviour, since building a full inheritance graph
is out of scope for this script. A legitimate no-op virtual hook will false-positive here
and needs a `# gdlint: disable` style justification or a Decision if that becomes common.
"""
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
THRESHOLDS_PATH = Path(__file__).resolve().parents[3] / "config" / "thresholds.yaml"
SCAN_DIRS = ("src",)
FUNC_RE = re.compile(
    r"^(\s*)(?:static\s+)?func\s+(\w+)\s*\([^)]*\)\s*(?:->\s*\S+)?\s*:\s*(.*)$"
)
STUB_BODY_RE = re.compile(r"^\s*(pass|push_error\(.*\)|assert\(\s*false\b.*\))\s*$")


def load_thresholds() -> dict:
    with THRESHOLDS_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def extract_functions(lines: list[str]) -> list[tuple[str, list[str]]]:
    """Return (function_name, body_lines) for each top-level function in the file."""
    functions = []
    current_name = None
    current_indent = None
    current_body: list[str] = []
    for line in lines:
        match = FUNC_RE.match(line)
        if match:
            if current_name is not None:
                functions.append((current_name, current_body))
            inline_body = match.group(3).strip()
            if inline_body:
                # Single-line body (e.g. `func a(): pass`) - already complete.
                functions.append((match.group(2), [inline_body]))
                current_name = None
                current_body = []
                continue
            current_indent = len(match.group(1))
            current_name = match.group(2)
            current_body = []
            continue
        if current_name is not None:
            is_body_line = line.strip() == "" or (
                len(line) - len(line.lstrip(" \t")) > current_indent
            )
            if is_body_line:
                if line.strip():
                    current_body.append(line.strip())
            else:
                functions.append((current_name, current_body))
                current_name = None
                current_body = []
    if current_name is not None:
        functions.append((current_name, current_body))
    return functions


def is_stub(body: list[str]) -> bool:
    non_comment_lines = [line for line in body if not line.startswith("#")]
    if len(non_comment_lines) != 1:
        return False
    return bool(STUB_BODY_RE.match(non_comment_lines[0]))


def main() -> int:
    thresholds = load_thresholds()
    max_methods = thresholds["solid_mechanical"]["isp"]["max_interface_methods"]

    violations = []
    for scan_dir in SCAN_DIRS:
        directory = REPO_ROOT / scan_dir
        if not directory.exists():
            continue
        for gd_file in directory.rglob("*.gd"):
            lines = gd_file.read_text(encoding="utf-8").splitlines()
            functions = extract_functions(lines)
            rel_path = gd_file.relative_to(REPO_ROOT)

            if len(functions) > max_methods:
                violations.append(
                    f"{rel_path}: {len(functions)} methods (budget: {max_methods}) "
                    f"[isp-method-count]"
                )

            for name, body in functions:
                if is_stub(body):
                    violations.append(
                        f"{rel_path}: {name}() body is a stub ({body[0]!r}) "
                        f"[isp-stub-detection]"
                    )

    if violations:
        print("ISP violations:")
        for violation in violations:
            print(f"  - {violation}")
        return 1

    print("isp-method-count / isp-stub-detection: no violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
