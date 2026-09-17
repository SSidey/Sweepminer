---
doc: templates/pr-description
status: active
---

# PR Description Template

```markdown
## Summary

<one or two sentences: what changed and why>

## Specification

<link to the spec this PR implements, if any>

## Run-baseline rubric

- [ ] `tests-red-then-green` — red→green log attached or linked
- [ ] `contract-tests-pass` (if applicable)
- [ ] `coverage-overall` ≥ threshold
- [ ] `coverage-changed-lines` ≥ threshold
- [ ] `lint-clean`
- [ ] `srp-size` / `ocp-shotgun-surgery` / `isp-method-count` / `isp-stub-detection` /
      `dip-direction` / `naming-grep-discoverable` / `no-cross-cutting-helper-violation`
- [ ] `progress-trend` — no regression vs. baseline (see attached log entry)
- [ ] `commit-message-conforms` / `branch-name-conforms`

CI reports these automatically; this checklist is for the human reviewer's visibility,
not a manual re-check.

## Progress log entry

<before/after metric table from `principles/progress-tracking.md` Gate 1, or a link to
the automated log entry>

## Human qualitative review (Gate 2)

- **Reviewer:**
- **Verdict:** <does this feel like genuine progress, independent of the numbers above?>
- **Notes:**

## Decisions

<link to any new or superseding Decision entries this PR introduces>
```
