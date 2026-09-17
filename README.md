# Sweepminer

A turn-based tunneling roguelike-lite. You descend through floors, excavating blind and
reading Minesweeper-style adjacency numbers to find what's around you. Combat hazards you
dig into become tactical battles — mostly auto-resolving, with a directly-controlled hero
as the one place player skill lives each round. Cleared ground becomes territory you fund
and fortify with resources banked along the way. Pressure comes from three interacting
systems: each floor's **nodes** emit threats faster the more you disturb the ground, a
**rival tunneler** advances on an unseen path with only ambiguous warning cues, and
**floor awakening** stops old floors from staying a permanently safe farm once you've
outgrown them. A chosen **Faction** and **Ruler** shape how you source population and what
the run occasionally demands of you.

Full design detail lives in [`sweepminer-spec-v0.3.md`](sweepminer-spec-v0.3.md),
including the running `## Decisions` log of choices made to unblock implementation.

## Status

**Phase 0 (environment & tooling scaffold) — done.** Git, the `dev_kit/` methodology kit,
and the GDScript tooling layer (GdUnit4, gdtoolkit, pre-commit, CI) are all wired up and
green. **Phase 1 (first playable vertical slice) — in progress.** There is no playable
build yet — this section and "Playing the game" below will be updated as soon as there is
one.

## Roadmap

- **Phase 0 — Environment & tooling** (done): git, `dev_kit/ci/godot/` tooling layer,
  CI.
- **Phase 1 — Vertical slice** (in progress): dig a small floor tile-by-tile, hit a
  combat hazard (resolved via a numeric auto-resolve stub, not the full battlefield yet),
  bank resources from land tiles, build one fortification, watch a node clock and
  Stability tick, and see a floor awaken on a blind vertical dig — all playtestable in the
  Godot editor.
- **Phase 2+ — depth passes** (not started; each has open decisions flagged in the
  spec's Section 7 that need resolving first):
  - The real tactical NxN battlefield (terrain, claiming vs. counter-claim fights,
    commanders, hero abilities) replacing the Phase 1 combat stub.
  - Node clearing curve tuning (real numbers, not the placeholder).
  - Industrialization as a second disturbance axis.
  - The rival tunneler and its warning cues.
  - Additional Factions/Rulers beyond the one built in Phase 1, and the
    roaming/organic-spread base models.
  - Whether fortification investment persists across runs (explicitly undecided).

This roadmap is kept current here as each phase lands — check the spec's Decisions
section for the reasoning behind any choice made along the way.

## Playing the game

Not yet possible — Phase 1 hasn't produced a playable scene. Once it does, this section
will explain how to get a running build (editor or exported binary). In the meantime, to
open the current scaffold:

1. Install [Godot](https://godotengine.org/download) **4.7.2** (stable).
2. Clone this repo.
3. Open `project.godot` in the Godot editor.

## Development

This project follows the AI-first / SOLID-mechanical dev kit in [`dev_kit/`](dev_kit/) —
see [`dev_kit/README.md`](dev_kit/README.md) for the principles and rubrics, and
[`dev_kit/ci/godot/README.md`](dev_kit/ci/godot/README.md) for how those rubrics map to
actual GDScript tooling.

```powershell
# One-time setup
pip install -r requirements-dev.txt
pre-commit install --install-hooks -t pre-commit -t commit-msg

# tools/local.env (gitignored) needs your local Godot binary:
#   GODOT_BIN=C:\path\to\Godot.exe

# Run the full test suite
pwsh dev_kit/ci/godot/scripts/run_tests.ps1
```
