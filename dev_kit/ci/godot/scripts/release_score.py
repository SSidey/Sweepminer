#!/usr/bin/env python3
"""Compute the Release Readiness Score for a versioned playtest entry.

Decision 5 in sweepminer-spec-v0.3.md scopes this composite score to release-level
playtest reporting only - it does not replace or contradict
dev_kit/principles/progress-tracking.md's Gate 1, which deliberately keeps per-PR
mechanical metrics unreduced to a single number. This score answers a different question
("is this version worth a human's time to play?"), not "did this specific PR regress
anything?" (that's what dev_kit/progress-log.md is for).

Formula, documented plainly so the number is never a black box:
    score = 60 * automated_checks_ratio + 40 * test_pass_ratio

- automated_checks_ratio: the "Automated checks passing" fraction from the release's
  dev_kit/progress-log.md row (e.g. 6/6 -> 1.0).
- test_pass_ratio: passed/total from that CI run's GdUnit4 JUnit report. If no tests
  exist yet (total == 0), this is treated as 0.0, not excluded - a version with no tests
  is not "ready," and the score should say so rather than hide the gap.

Coverage is deliberately not in this formula: no confirmed GdUnit4 coverage CLI flag
exists yet (see dev_kit/ci/godot/README.md), and this score doesn't fake a number it
can't measure.
"""
AUTOMATED_CHECKS_WEIGHT = 60
TEST_PASS_WEIGHT = 40


def compute_score(automated_checks_ratio: float, test_pass_ratio: float | None) -> dict:
    automated_component = AUTOMATED_CHECKS_WEIGHT * automated_checks_ratio

    if test_pass_ratio is None:
        test_component = 0.0
        test_note = "no tests yet"
    else:
        test_component = TEST_PASS_WEIGHT * test_pass_ratio
        test_note = f"{test_pass_ratio:.0%} of tests passing"

    return {
        "score": round(automated_component + test_component, 1),
        "automated_checks_component": round(automated_component, 1),
        "test_component": round(test_component, 1),
        "test_note": test_note,
    }
