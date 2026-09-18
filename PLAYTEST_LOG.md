# Playtest & Human Qualitative Review Log

This is the file to edit for subjective play-feel notes. It implements Gate 2 of
[`dev_kit/principles/progress-tracking.md`](dev_kit/principles/progress-tracking.md): the
human qualitative verdict, recorded separately from the mechanical
[`dev_kit/progress-log.md`](dev_kit/progress-log.md), and **never filled in by the
implementing agent**, since an agent judging its own change has an obvious conflict of
interest.

## How entries get here

Per Decision 5 in [`sweepminer-spec-v0.3.md`](sweepminer-spec-v0.3.md), a new dated entry
is generated automatically — not written by hand, and not one per PR — whenever a merge to
`main` warrants a version bump (any `feat`/`fix`/breaking-change commit since the last
release tag; a `chore`-only merge has nothing new to play, so it produces no entry).
[`.github/workflows/release.yml`](.github/workflows/release.yml) tags the release,
computes the mechanical **Release Readiness Score**, appends the stub entry below via
`dev_kit/ci/godot/scripts/generate_release_playtest_entry.py`, and opens a PR with just
that addition for you to merge.

**Your job per entry:** play that version, then fill in the blank fields — Functional
rating, Fun/engagement rating, the bug table, and session notes. Never edit a prior
entry's *filled-in* fields after the fact; if your assessment of an old version changes,
add a note under a new entry rather than rewriting history.

## What the mechanical score does and doesn't mean

`score = 60 × automated_checks_ratio + 40 × test_pass_ratio` (see
`dev_kit/ci/godot/scripts/release_score.py` for the exact computation). It tells you
whether the *build* is sound — checks passing, tests green. It says nothing about whether
the game is any good. That's exactly what the fields below are for.

## Entry template (for reference — real entries are auto-generated in this shape)

```markdown
### v<version> — <date>

**Mechanical (Release Readiness Score): <score>/100**
- Automated checks: <N>/<M> (<component>/60)
- Tests: <pass ratio or "no tests yet"> (<component>/40)
- Full metrics: see `dev_kit/progress-log.md`, ref `<ref>`

**Functional rating (1-5):** _fill in after playtesting_
**Fun/engagement rating (1-5):** _fill in after playtesting_

**Bug entries:**

| Severity | What happened | Repro steps |
|---|---|---|
| _blocker / major / minor_ | | |

**Session/completion notes:** _fill in after playtesting_
```

---

<!-- Auto-generated entries below this line. Newest at the bottom. -->
