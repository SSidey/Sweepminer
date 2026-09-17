# AI-First Development Kit — Documentation Layer

This is the **stack-agnostic** layer of a two-layer starter kit for AI-driven,
quality-gated software development. It defines principles and rubrics that do not
depend on any particular language, framework, or engine. A separate,
**stack-specific implementation layer** (starting with Godot 4 / GDScript, in
`ci/godot/`, once built) wires these rubrics into actual tooling: linters, coverage
tools, contract-test runners, and CI/pre-commit configuration.

This kit is independent of any other project-specific tooling — it introduces no
shared terminology, file paths, or dependencies beyond what is documented here, and is
intended to be dropped into any greenfield project as-is.

## Layout

```
principles/
  ai-first-organisation.md   Four file-organisation principles (concern, locality,
                              naming, no cross-cutting helpers)
  solid-mechanical.md        SOLID as mechanical checks + honestly-scoped manual review
  decision-ledger.md         Append-only decision convention
  progress-tracking.md       Mechanical hard gate + separate human qualitative gate
  tdd-bdd-workflow.md        Behaviour-first workflow, spec-type taxonomy, coverage floor

rubrics/
  spec-baseline.rubrics.md   Checked when a specification is authored
  run-baseline.rubrics.md    Checked at the end of every implementation pass

templates/
  decision-entry.md          Copy-paste blocks for new/superseding decisions
  commit-message.md          Conventional Commits template + type-vs-diff correctness
  pr-description.md          PR template linking rubric checklist + progress log

config/
  thresholds.yaml            All configurable numeric thresholds in one place
```

## Reading order for a new project

1. `principles/ai-first-organisation.md` and `principles/solid-mechanical.md` — the
   design rules everything else enforces.
2. `principles/tdd-bdd-workflow.md` — how behaviour gets specified and implemented.
3. `principles/decision-ledger.md` and `principles/progress-tracking.md` — how the
   project records its own history and trend.
4. `rubrics/spec-baseline.rubrics.md` and `rubrics/run-baseline.rubrics.md` — the
   checklists that tie 1–3 into concrete pass/fail gates.
5. `templates/` — the boilerplate you'll actually copy while working.
6. The stack-specific `ci/<stack>/` layer (not yet built) — how the rubrics in step 4
   actually get executed, locally and in CI, for your chosen language/engine.

## Versioning note

This kit itself is a set of specifications. Changes to any file here follow the same
rules it defines for everything else: a `policy`-type spec, changes to a Decision are
append-only, and any threshold change in `config/thresholds.yaml` needs a recorded
Decision.
