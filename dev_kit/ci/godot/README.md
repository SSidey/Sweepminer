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
| `no-cross-cutting-helper-violation` | `scripts/check_helper_promotion.py` | run via `pre-commit` and CI |
| `commit-message-conforms` | `pre-commit` hook (Conventional Commits regex) | `.pre-commit-config.yaml` |
| `branch-name-conforms` | procedural, via `.claude/skills/run-phase/SKILL.md` | see "Procedural, not scripted" below |
| `ocp-shotgun-surgery` | `scripts/check_ocp_shotgun_surgery.py` | CI only (needs a diff vs. the PR base ref — see below) |
| `isp-method-count` / `isp-stub-detection` | `scripts/check_isp.py` | run via `pre-commit` and CI |
| `dip-direction` | `scripts/check_dip_direction.py` | run via `pre-commit` and CI |
| `progress-trend` | `scripts/run_tests.ps1` output diffed against the prior progress-log entry by hand | see `principles/progress-tracking.md` |

## Heuristic limits (stated plainly, not hidden)

Per `principles/solid-mechanical.md`'s own convention of honestly labeling what a check
does and doesn't prove, these four scripts are real mechanical checks but each is a
heuristic, documented in its own docstring — read it before trusting a green run blindly:

- `check_isp.py` — stub-detection flags *any* trivial function body, not only true
  overrides of a base method with real behaviour (no inheritance graph is built). A
  legitimate no-op virtual hook will false-positive.
- `check_ocp_shotgun_surgery.py` — counts pre-existing `src/` files modified in this
  diff; it cannot distinguish "one new case forced N files open" from any other reason N
  files changed together (e.g. a deliberate, justified refactor). Only runs in CI, since
  it needs a diff against the PR's base ref, not just the working tree.
- `check_dip_direction.py` — enforces this project's own domain/infrastructure boundary
  (`src/` = engine-agnostic, `scenes/` = Godot glue) via `extends` and
  `preload`/`load` keyword scanning, not a full call-graph analysis.
- `check_helper_promotion.py` — only catches the catch-all-filename shape of the
  violation (`utils.gd`, `helpers.gd`, `common.gd`, `base.gd`, `manager.gd`); it can't
  detect a helper duplicated past the promotion threshold without call-graph tooling.

Automating past these heuristics (a real call-graph/AST tool for GDScript) is future work,
not a gap papered over with a script that always passes.

## Procedural, not scripted

- `branch-name-conforms` — no mechanical linter; enforced procedurally instead via
  `.claude/skills/run-phase/SKILL.md`, which always branches with a purpose-driven
  Conventional Branch prefix (`feature/`, `fix/`, `hotfix/`, `release/`, `chore/`) before
  any implementation work starts.

## Running the checks locally

```powershell
# Lint + format check (matches CI's lint job)
gdlint src tests
gdformat --check src tests

# Size-budget, naming, ISP, DIP, and helper-promotion checks
python dev_kit/ci/godot/scripts/check_size_budgets.py
python dev_kit/ci/godot/scripts/check_naming.py
python dev_kit/ci/godot/scripts/check_isp.py
python dev_kit/ci/godot/scripts/check_dip_direction.py
python dev_kit/ci/godot/scripts/check_helper_promotion.py

# OCP shotgun-surgery (diff-scoped, defaults to comparing against origin/main)
python dev_kit/ci/godot/scripts/check_ocp_shotgun_surgery.py [base-ref]

# Full test suite + coverage (requires GODOT_BIN — see tools/local.env)
pwsh dev_kit/ci/godot/scripts/run_tests.ps1
```

`pre-commit` runs the fast checks (lint, format, size, naming) on every commit. The full
test+coverage run is deliberately excluded from pre-commit (too slow per-commit) and
instead run on demand locally and authoritatively in CI — see
`rubrics/run-baseline.rubrics.md`'s "Where this runs" section.
