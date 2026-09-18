---
name: run-phase
description: "Implement one phase of an approved Sweepminer execution plan end-to-end, following dev_kit's branch/commit conventions and TDD/rubric workflow. Use when asked to implement, start, or continue a plan phase (e.g. \"do Phase 1\", \"implement the vertical slice\", \"continue where we left off\"), or when invoked as /run-phase. Do not use for one-off fixes unrelated to a plan phase, or for exploratory/research-only requests."
---

# Implementing a plan phase

This codifies the standing process for turning one phase of an approved execution plan
(e.g. `sweepminer-spec-v0.3.md`'s Decisions-backed roadmap, or a plan file under
`C:\Users\Simeon\.claude\plans\`) into merged, rubric-compliant work. It exists so every
phase follows the same discipline instead of re-deriving it each time — see
`dev_kit/README.md`'s reading order for the principles this enforces.

**Standing rule, not phase-specific: nothing lands on `main` directly.** Every change,
regardless of size, goes on its own branch and through a PR that a human merges.

## 0. Identify the phase

- If an argument names the phase or plan file, use it. Otherwise ask the user which phase
  to implement (don't guess against a stale plan).
- Read the phase's scope in full before starting — the relevant plan file, and
  `sweepminer-spec-v0.3.md`'s `## Decisions` section for any constraint already recorded
  that bears on this phase.
- Confirm the working tree is clean (`git status`) and `main` is up to date
  (`git checkout main && git pull`) before branching. If there are uncommitted changes
  that aren't yours to discard, stop and ask.

## 1. Branch — Conventional Branch, purpose-driven prefix only

Per this project's decision, branch names use purpose-driven prefixes only (no
`claude/`-style agent-source prefix): `feature/`, `fix/` (bugfix), `hotfix/`, `release/`,
or `chore/`, followed by a lowercase-kebab-case description. No consecutive/leading/
trailing hyphens, no underscores or spaces — see
[conventionalbranch.org](https://conventionalbranch.org/) for the full grammar.

Pick the prefix by what the phase's diff actually is, same judgement as the commit-type
table in `dev_kit/templates/commit-message.md`:
- New gameplay capability (most plan phases) → `feature/`
- Correcting broken behaviour → `fix/`
- Tooling/CI/process only, no gameplay behaviour → `chore/`

```
git checkout main
git pull
git checkout -b feature/<short-kebab-slug-for-this-phase>
```

## 2. Implement via the dev_kit TDD workflow

Follow `dev_kit/principles/tdd-bdd-workflow.md` for every code-bearing step in the phase,
in the order the plan lays out (usually bottom-up: lower-level modules whose tests don't
depend on anything not yet built, first):

1. State the behaviour as Given/When/Then before writing any implementation.
2. Write the GdUnit4 test first, under `tests/`, mirroring the `src/` path being tested.
3. Run it and confirm **red** — it must fail for the right reason (missing behaviour, not
   a typo). Use `pwsh dev_kit/ci/godot/scripts/run_tests.ps1` or the GdUnit4 editor
   inspector.
4. Implement the minimum to go **green**. Do not implement behaviour with no test.
5. Refactor with the suite as a safety net, checking against
   `dev_kit/principles/ai-first-organisation.md` and
   `dev_kit/principles/solid-mechanical.md` as you go (one concern per file, size
   budgets, no cross-cutting helpers below the promotion threshold).
6. Where the phase introduces a second implementation of an existing base
   type/interface/contract, write the shared contract-test suite once and run it
   unmodified against every implementation (`solid-mechanical.md` criterion L) — do not
   write a bespoke test per implementation instead.

**If the plan is ambiguous or hits a decision point it doesn't already resolve**, stop and
interview the user (don't assume). Once resolved, append a new Decision entry to
`sweepminer-spec-v0.3.md`'s `## Decisions` section using
`dev_kit/templates/decision-entry.md` — never edit a prior Decision's text, only append
(and mark superseded ones per `dev_kit/principles/decision-ledger.md` if applicable).

## 3. Commit as you go

Before each commit, run the fast local gate: `pre-commit run` (runs automatically on
`git commit` once installed, but run it manually first if you want to see failures
before staging). Write commit messages per `dev_kit/templates/commit-message.md` —
Conventional Commits, with the type matching the actual diff, not the intent (a
`refactor` with behaviour-asserting test changes is actually a `feat` or `fix`; split the
commit if the diff genuinely mixes types).

## 4. End-of-phase gate (before opening a PR)

This is `dev_kit/principles/progress-tracking.md` Gate 1 — mechanical, hard, and not
skippable:

1. Run the full suite: `pwsh dev_kit/ci/godot/scripts/run_tests.ps1`.
2. Run the static checks: `check_size_budgets.py`, `check_naming.py`, `check_isp.py`,
   `check_dip_direction.py`, `check_helper_promotion.py`, and
   `check_ocp_shotgun_surgery.py origin/main` (all under
   `dev_kit/ci/godot/scripts/`) — these also run in `pre-commit`/CI, but run them
   directly here to catch anything before pushing.
3. Run `python dev_kit/ci/godot/scripts/report_progress.py "<branch-name>"` — this
   computes the current metrics, diffs them against the previous row in
   `dev_kit/progress-log.md`, and appends the new row itself. **A non-zero exit means a
   regression was detected; the phase is not done until that's fixed** — loop back into
   step 2 rather than opening a PR on a known regression. Coverage still isn't in this
   script (see its docstring) — check it manually via the GdUnit4 editor inspector and
   note the number when filling in the PR.
4. Read each static check's heuristic-limit note in
   `dev_kit/ci/godot/README.md` ("Heuristic limits") before trusting a green run
   blindly — a pass means the specific heuristic found nothing, not that the underlying
   SOLID property is proven.
5. Update `README.md`'s **Status** and **Roadmap** sections to reflect the phase's actual
   completion state — this is a standing part of finishing a phase, not optional polish.
6. Append a stub entry to `PLAYTEST_LOG.md` for this PR (title, date, a blank
   **Verdict**/**Play feel notes**) using its own template section — leave the content
   blank for the user to fill in; do not write play-feel judgements yourself, same
   conflict-of-interest reasoning as Gate 2 generally.

## 5. Open the PR — do not merge it

Push the branch and open a PR with `gh pr create`, body from
`dev_kit/templates/pr-description.md`: summary, link to the spec/plan, the rubric
checklist from step 4, and for the two Gate sections:
- **Progress log entry** — link to the row `report_progress.py` just appended to
  `dev_kit/progress-log.md` (quote it inline too, so the reviewer doesn't have to open
  another file).
- **Human qualitative review (Gate 2)** — link to the stub entry just added to
  `PLAYTEST_LOG.md`, rather than filling Reviewer/Verdict/Notes inline. That gate is
  explicitly not something the implementing agent fills in for itself
  (`progress-tracking.md`: "an agent judging whether its own change was an improvement
  has an obvious conflict of interest").

Per this project's decision, **stop here.** Report the PR URL and a short summary of what
landed; the user reviews and merges. Do not merge, even if CI is green.
