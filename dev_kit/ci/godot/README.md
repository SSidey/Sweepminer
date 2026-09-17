---
doc: ci/godot/README
status: active
applies_to: the Godot 4 / GDScript implementation of this project
---

# Godot / GDScript Tooling Layer

This directory wires the stack-agnostic rubrics in `rubrics/run-baseline.rubrics.md` and
`rubrics/spec-baseline.rubrics.md` into actual tools for a Godot 4 / GDScript project. It
is the implementation layer the top-level `dev_kit/README.md` describes as "not yet
built" — this is that build.

## Rubric → tool mapping

| Rubric row | Tool | Where |
|---|---|---|
| `lint-clean` | `gdlint` (gdtoolkit) | `.gdlintrc` (repo root — gdlint auto-discovers it by walking up from cwd, no `--config` flag exists), run via `pre-commit` and CI |
| formatting (supports `lint-clean`) | `gdformat` (gdtoolkit) | run via `pre-commit` and CI |
| `tests-red-then-green` | GdUnit4 CLI | `scripts/run_tests.ps1`, CI workflow |
| `contract-tests-pass` | GdUnit4 CLI, same test run as above | shared contract-test suites live under `tests/**/test_*_contract.gd` by convention |
| `coverage-overall` / `coverage-changed-lines` | GdUnit4 built-in coverage report | `scripts/run_tests.ps1` (`-c` coverage flag), threshold checked against `config/thresholds.yaml` |
| `srp-size` | `scripts/check_size_budgets.py` | run via `pre-commit` and CI |
| `naming-grep-discoverable` | `scripts/check_naming.py` | run via `pre-commit` and CI |
| `no-cross-cutting-helper-violation` | manual review for now | see "Not yet automated" below |
| `commit-message-conforms` | `pre-commit` hook (Conventional Commits regex) | `.pre-commit-config.yaml` |
| `branch-name-conforms` | procedural, via `.claude/skills/run-phase/SKILL.md` | see "Not yet automated" below |
| `ocp-shotgun-surgery` | manual review for now | see "Not yet automated" below |
| `isp-method-count` / `isp-stub-detection` | manual review for now | see "Not yet automated" below |
| `dip-direction` | manual review for now | see "Not yet automated" below |
| `progress-trend` | `scripts/run_tests.ps1` output diffed against the prior progress-log entry by hand | see `principles/progress-tracking.md` |

## Not yet automated (stated plainly, not faked)

Per `principles/solid-mechanical.md`'s own convention of honestly labeling unautomated
checks rather than inventing a hollow tool for them, the following rubric rows have **no
mechanical check yet** in this project and are reviewed manually at the end of each
implementation pass, by reading the diff against the stated question:

- `ocp-shotgun-surgery` — does this diff touch ≥3 pre-existing files to add one new
  case/behaviour?
- `isp-method-count` / `isp-stub-detection` — does any interface exceed 7 methods, or does
  any implementer have a not-implemented/no-op stub body?
- `dip-direction` — does any `src/**` domain file `preload`/`extends` a low-level/engine
  concern it shouldn't (this project doesn't yet separate "domain" vs. "infrastructure"
  directories formally, so this is judgement-only until that separation exists)?
- `branch-name-conforms` — no mechanical linter yet; enforced procedurally instead via
  `.claude/skills/run-phase/SKILL.md`, which always branches with a purpose-driven
  Conventional Branch prefix (`feature/`, `fix/`, `hotfix/`, `release/`, `chore/`) before
  any implementation work starts.

Automating these (a call-graph/AST tool for GDScript) is real future work, not a gap to
paper over with a script that always passes.

## Running the checks locally

```powershell
# Lint + format check (matches CI's lint job)
gdlint src tests
gdformat --check src tests

# Size-budget and naming checks
python dev_kit/ci/godot/scripts/check_size_budgets.py
python dev_kit/ci/godot/scripts/check_naming.py

# Full test suite + coverage (requires GODOT_BIN — see tools/local.env)
pwsh dev_kit/ci/godot/scripts/run_tests.ps1
```

`pre-commit` runs the fast checks (lint, format, size, naming) on every commit. The full
test+coverage run is deliberately excluded from pre-commit (too slow per-commit) and
instead run on demand locally and authoritatively in CI — see
`rubrics/run-baseline.rubrics.md`'s "Where this runs" section.
