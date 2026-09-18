---
spec_type: hybrid
status: active
---

11# Sweepminer — Consolidated Design Spec v0.3

A tunneling roguelike-lite: descend through floors, excavate blind using adjacency clues, gather resources and minions, fortify what you've claimed, and resolve threats as tactical battles fought on the tile you dug into. Exploration is deliberate and turn-based; combat is tactical and mostly auto-resolving, with a hero as the one directly piloted piece. Pressure comes from a set of interlocking systems — nodes, disturbance, and a floor-awakening mechanic — that punish both rushing and lingering.

---

## 1. High-Level Structure

- A run descends through a sequence of **floors**. Each floor is tunneled from an entry point.
- Floors are cleared through **exploration** (tactical, turn-based, Minesweeper-style adjacency digging).
- Combat hazard tiles become their own **tactical battlefield** — a pre-authored NxN arena, resolved mostly automatically with the player's hero as the active layer of control.
- Cleared tiles become buildable **territory**, using a hybrid of fixed terrain-defined anchor spots and free placement.
- Pressure comes from **nodes** (a per-floor emission clock), a **rival tunneler** and other roaming threats, and a **floor-awakening** mechanic that stops old floors from staying safe forever.
- A **Faction** (chosen at run start) and a **Ruler** (layered on top) shape population sourcing, base model, and personal quirks for that run.

---

## 2. Exploration Layer (Tactical)

### Tunneling
- You dig tile-by-tile, always from a tile adjacent to one you've already opened — a literal path, not a free pick.
- Every opened tile shows a **number**: count of hazard-type tiles adjacent to it (Minesweeper logic). Empty tiles are not wasted — the number is the reward.
- No fog outside what's adjacent to opened ground — you cannot see ahead further than one tile's neighbors.
- Detection is **lateral only** — your adjacency sense reads the plane you're standing on, not what's beneath it. This is the reason digging straight down is inherently blind (see Section 4, Vertical Digging).

### Tile Types
| Type | Behavior |
|---|---|
| **Combat hazard** | Triggers a tactical battlefield encounter immediately on excavation (Section 4). Win → the encounter becomes a Minion in the Stack. Lose → direct cost to Stability/resources. |
| **Environmental hazard (flood/lava)** | Does not resolve as combat. Instead seeds a **spreading front** (see below). |
| **Land/Resource** | Safe. Banks currency used for upgrades, repairs, and fortifications. |
| **Treasure** | Rare. A guaranteed strong minion, an item, or occasionally a hero. |
| **Empty** | No reward beyond its adjacency number. |

### Environmental Hazards (Flood / Lava)
- Once triggered, the front advances roughly one tile per turn from its origin, permanently sealing tiles behind it (they can no longer be dug or crossed).
- This is a **tempo** pressure, distinct from combat's **judgment** pressure: you can't out-skill a flood front, only out-pace it or wall it off.
- **Blockages** can be built (from banked resources) on any excavated tile to halt a front's advance in that direction — the same underlying system as combat defenses (Section 3): hazard-sealing and defense-building are one mechanic wearing two hats.
- Some chasms are pure hazards that do not reach the floor below — a battlefield obstacle only, no shortcut implied. Others do connect downward (see Section 4).

### The Muster Stack (Push-Your-Luck)
- Minions gained from cleared combat hazards join an ordered **Stack**.
- Adding a minion risks a **collapse**: chance scales inversely with Stability (a worn-down resource, degrades in small permanent steps, rarely repaired).
- On collapse, the top (most recent) minion is lost, plus a Stability penalty — reframed thematically as a **cave-in**, fitting the tunneling setting directly.
- Stability is the run's slow-burn resource: it doesn't reset floor to floor, and hitting 0 ends the run.
- Tiles dug but left unsupported (no wall/support built) also strain Stability over time — neglect has the same cost as an unlucky muster roll. This is the core reason rushing straight down without ever stopping to build is unsustainable: it's spending Stability faster than it can be recovered.

---

## 3. Territory & Fortification

A cleared tile becomes buildable ground, using a hybrid placement model rather than either fully free-form or fully fixed construction.

### Anchor Spots vs. Free Cells
- **Anchor spots** — fixed, terrain-defined, non-negotiable. A resource seam sits on a specific cell; its extraction structure must be built there and nowhere else. A chasm's supports must be built on the chasm's own cells before anything can be built across it. The player chooses *whether* to invest, not *where* the feature is.
- **Free cells** — genuinely open, flat, unclaimed ground. Structures with a footprint (e.g., a 2×2 barracks) can be placed anywhere there's enough contiguous open space.

### Terrain Effects on Placement
- **Elevation (ramps, pillars)** grants a persistent combat bonus (vision/ranged) that is **not** removed by building on it. However, uneven terrain restricts *which* structures can be placed there — most structures require flat ground; a narrow set (e.g., a blockade) can be built on a ramp specifically. This makes holding elevation and fortifying it partially competing goals.
- **Broad chasms** require bridging before the cells they occupy become buildable or crossable.
- Changing terrain or building on it costs **finite resources** — this is the primary reason to keep descending: local resources run out, and going deeper is how you fund further consolidation.

### Defenses & Blockages
- **Blockages** — seal a tile against environmental fronts, or block a path outright.
- **Defenses** — structures with their own HP that absorb or weaken incoming threats.
- Fortifying a floor turns "the rival/flood is coming" into a manageable timeline instead of a fixed countdown.
- Open question: does fortification investment persist across runs in any meta-progression sense? Not yet decided.

---

## 4. Combat: Tactical Tile-Battlefield

Each combat hazard tile is a pre-authored **NxN battlefield** — terrain features (pillars, chasms, elevation, a lava floor) and an inhabited structure (a hive, nest, den) that defines both the look of the tile and what's fighting you there. Terrain and enemy identity are the same authored content, not two separate layers.

### Two Distinct Fight Types
- **Claiming fight** — first contact with a tile's native terrain and inhabitants, fought on unmodified ground. The tile's authored identity does the work here: a lava-floor hive plays nothing like a pillar-heavy chasm nest, before anything has been built.
- **Counter-claim fight** — a later defense of a tile you've since built on. The terrain is now partly yours (walls, garrisons, chokepoints layered over the original features), and this is where commander stakes (below) matter most, since you have units to actually lose control of.
- Early tiles skew toward claiming fights (novel terrain, discovery); held territory skews toward counter-claims (defense-in-depth, testing what you've built). The same battlefield system produces two different emotional beats.

### Resolution Model
- The bulk of a fight — garrisoned units, formations, structures — **resolves automatically** each round based on stats and positioning (Conquest of Elysium-style): fast, no per-soldier micromanagement, so counterpushes read as immediate rather than a slow back-and-forth.
- The **hero** is the one directly controlled piece: attacks, uses abilities, repositions a garrison, or reinforces a wall mid-fight, each as an active choice each round. This is where player skill actually lives — everything else is automatic specifically so the hero's actions can matter.
- Building/reinforcing mid-fight is a hero action that competes with attacking for that round — fortification stays tense and reactive rather than a calm pre-battle chore.

### Commanders
- A unit needs an assigned **commander** to receive active player orders during a fight.
- If a unit's commander is killed, that unit reverts to its **preset orders** (configured before the battle, or a sensible default) rather than going inert — control is lost, not the unit's ability to act.
- This makes commander placement a real pre-fight decision: where you station commanders determines what you can still influence if one falls.

### Vertical Digging
- Because detection is lateral-only (Section 2), digging straight down is always blind — no adjacency information exists for what's beneath you.
- Established downward routes (stairs, or a chasm confirmed to connect to the floor below) are the only *verified* paths — they were dug and checked tile-by-tile under the same lateral detection at some point.
- **Two ways down, both viable:**
  - **Blind vertical dig** — fast, unscouted, no defenders, but the destination is unknown and the disturbance effect is immediate (Section 5).
  - **Guardian-defended route** (a proper stairwell or a connecting chasm) — pre-authored, defensible terrain guarding a confirmed safe path. Must be fought and cleared before it's usable. Worth it for the fight's own rewards and a genuinely secured, fortifiable route — not because it avoids consequence (see Awakening, Section 5).

### Floor Assaults / Back-to-Back Encounters
- A major assault (a "boss base," or the rival tunneler's arrival) is expressed as a sustained sequence of encounters without a full reset between them, rather than a single harder fight.

---

## 5. Pressure & Threats

### Nodes
- Each floor has **N nodes**, each emitting threats at rate **R**. The floor's implicit goal is to clear as many nodes as possible in as few digs as possible — every dig is a resource spend against a clock that's actively getting worse.
- Digging activity (spatial disturbance) increases R.
- **Clearing curve (untuned):** the reward for clearing an additional node should decay as more are cleared, while the cost to reach remaining nodes should rise. Tuned correctly, "good enough" partial clearing beats greedy full-clearing by the shape of the curve, without needing an arbitrary cap. This needs real numbers-on-paper iteration, not a fixed rule.

### Threat Taxonomy (three distinct sources)
1. **Apparitions** — spawned by node activity, manifest directly onto already-open ground without needing to be dug into. These are what make a cleared tile unsafe over time.
2. **Active diggers** — the rival tunneler, plus potentially other digging entities (a giant worm, rival factions) that carve their own paths and can intrude into the player's tunnels from outside the player's own dig history.
3. **Hazard tiles** — the original combat/environmental hazards found by the player's own excavation (Section 2).

Each demands a different player skill: apparitions reward finishing/fortifying a tile before moving on; active diggers reward vigilance toward warning cues; hazard tiles reward careful adjacency reading.

### Rival Tunneler & Warning Cues
- Present from the start of a run, advancing on an unseen path.
- The player receives no direct view of the rival's position — only **ambiguous cues** (tremors, distant sounds) that could indicate the rival, a structural weakness, or an environmental front. The player should not be able to reliably tell which.
- Cue frequency/intensity is the primary tuning lever for "how close is too close."
- On contact, the rival triggers a Combat encounter (not an instant loss) — likely a hard fight, possibly a multi-wave assault.

### Industrialization (second disturbance axis)
- Independent from spatial disturbance (digging): **industrial disturbance** is driven by how hard already-claimed ground is being worked — extraction rate, structure density.
- Could scale a separate multiplier on node rate R, or wake something distinct entirely (deep-dwellers reacting to noise/vibration rather than to open ground).
- Trade-off framing for the player: depth gets you access to better resources, but extraction *rate* is what makes noise. A player can dig aggressively but industrialize lightly and stay quieter than their tunnel footprint suggests, or the reverse.

### Floor Awakening (anti-farming)
Awakening exists purely to stop old floors from being a permanently trivial farm once the player has outgrown them — it is not a cost the player is meant to strategically time or defer.

**Triggers (first to occur):**
1. A **blind vertical dig** on a floor awakens it immediately.
2. Defeating a **guardian force** on a defended route awakens the floor **on the next tile dug anywhere on that floor, the floor above it, or the floor below it** — not immediately, and not avoidable by leaving cleanly, since continuing to play at all will almost certainly involve digging on at least one of those three floors eventually.

**Effect:** An awakened floor's **apparition tier is set to exactly match the player's current maximum depth reached**, and continues tracking it — an awakened floor is always precisely as dangerous as the player's frontier, automatically, with no need to retrigger as the player goes deeper. This deliberately does not touch the floor's original native hazard content (no retroactive stat rescaling of fixed encounters); it only raises the tier of apparitions that spawn onto its open ground.

- A floor that is **never awakened** keeps only its original, already-substantially-cleared native hazards — genuinely safer, but also has little left worth farming if it was played properly the first time.
- There is no "clean window" once a route is secured via the guardian trigger — the floor above, the floor itself, and the floor below are all primed, and normal play will trip one of them.

---

## 6. Population, Faction & Ruler

### Population Sourcing (three channels, all usable to varying degrees regardless of faction)
- **Growth** — a birth/replenishment rate at the home base, fed by investment there (housing, food). Slow and compounding; creates a real allocation tension, since the same population pool that could become soldiers could instead stay civilian and keep growing the base faster.
- **Mercenaries** — currency-bought, immediate, no growth curve. Good for plugging a gap, resource-hungry indefinitely as a sole strategy.
- **Allied settlements found deeper** — an exploration reward. Can grant a population injection, a recruitment pool, or unique unit types unavailable elsewhere. Gives some factions a reason to descend for *people*, not just materials.

### Faction (chosen at run start — two largely independent identity axes)
Factions vary primarily along one dominant axis for legibility; combining strong identities on both risks feeling like two half-explained ideas rather than one clear one.

- **Population-sourcing axis:**
  - *Growth-reliant* — birth-rate dependent, strong incentive to invest in the home base early, population contested between labor and military.
  - *Constructed/metal-reliant* — no births; units are built directly from extracted resources. Scaling is gated entirely by extraction throughput, tying this faction tightly to the industrialization knob (Section 5).
  - *Settlement/mercenary-reliant* — light on home-base growth, leans on mercenaries early and allied-settlement integration long-term; this faction's core reason to descend is population, not materials.
- **Territory & base-model axis:**
  - *Fixed home base* — permanent, heavily fortified, the default assumption elsewhere in this spec.
  - *Roaming* — the base itself relocates; likely favors portable structures over permanent fortification, and may have a different relationship to floor-level disturbance/awakening since it isn't sitting in one place accumulating it.
  - *Organic spread* — passive, territorial growth into adjacent ground rather than discrete construction.

### Ruler
- Layered on top of Faction: a narrower, flavorful requirement or quirk (e.g., needing to secure a specific resource that demands extra exploration) rather than a structural change to the run.
- Faction changes the machine; Ruler changes what the machine occasionally demands of the player.

---

## 7. Explicitly Open / Untuned

- Node clearing curve — exact decay/cost math (flagged above as needing hands-on iteration).
- Industrialization's precise effect: a node-rate multiplier, a wholly separate wake source, or both.
- Full building/anchor catalog beyond resource seams and chasm supports.
- Full hero roster, abilities, and how many commanders a run typically has access to.
- Exact blockage/defense costs and HP values.
- Tremor/warning cue design — frequency, how ambiguous vs. informative they should feel.
- Whether fortification investment has any cross-run persistence.
- Full Ruler roster and their specific quirks beyond the one example given.
- How roaming and organic-spread factions interact with floor disturbance/awakening, given they don't hold ground the way a fixed base does.

---

## 8. Prototyping Recommendation

The combat resolution model (tactical, auto-resolve + hero control) is far cheaper to prototype than the rhythm/gesture alternative explored earlier (Appendix A) — there's no timing-critical input detection to get right, so it can be validated with simple turn-based logic before committing to any particular engine.

- **Exploration layer** (tunneling, adjacency numbers, muster stack, fortification, nodes/awakening) — cheap to paper-prototype or mock up in a spreadsheet; entirely turn-based, no timing component.
- **Tactical battlefield layer** — also reasonably cheap to test on paper or in a simple grid-based mockup first (does the claiming/counter-claim split feel different, does commander loss meaningfully change a fight), since the core tension is decision-based rather than reflex-based.
- If/when moving to a real engine, **Godot** remains a reasonable pick for a 2D grid-based tactics game generally (fast iteration, good for solo prototyping), but the specific reasons to prefer it in Appendix A (touch/gesture precision, sync-critical audio) no longer apply under this combat model.

---

## Appendix A: Alternative Combat Model Explored — Rhythm/Gesture (Superseded)

This system was designed in detail before the tactical tile-battlefield model (Section 4) was chosen instead. Kept here for reference in case a rhythm-based encounter type is ever reintroduced as a specific flavor of fight rather than the core resolution system.

### Threats & Coverage
- Each enemy in an encounter would run its own independent prompt stream.
- The number of units brought from the Stack would determine **coverage** — how many simultaneous threats the player could actively respond to.
- Threats beyond coverage would escalate (chip damage, shrinking windows) rather than queue passively.

### Gesture Types
- **Tap** — quick, precise-timing input.
- **Hold** — sustained input across a duration.
- **Sweep** — directional/path-based input.

### Baseline Verbs
| Verb | Gesture (typical) | Function |
|---|---|---|
| **Attack** | Tap | Offense, modified by type matchup (Brute/Swift/Arcane triangle). |
| **Defend** | Hold | Mitigates an incoming hit without a type match. |
| **Reposition / Create Distance** | Sweep | A spacing tool for dodging attacks that demand distance rather than a block — not disengagement from the encounter. |

### Extended Baseline Verbs
- **Fast Attack** — lower commitment, smaller reward, more forgiving timing.
- **Reckless Attack** — higher risk/reward, harsher miss penalty.
- **Buff** — supportive, spends or builds Momentum.

### Specials
- Units and heroes would carry unique gesture combos beyond the baseline set, gated behind a Momentum/Fever resource built from clean hits.

### Precision & Outcome
- Landed inputs would scale by accuracy (osu logic) — perfect, near-miss, or a clean miss that both fails the effect and applies a worse penalty than not acting.

### Escalation / Overwhelm
- Difficulty scaling would raise tempo and/or add simultaneous prompt streams beyond coverage, escalating gradually (shrinking windows, decoy prompts) rather than as a binary fail-state.

### Encounter Flow Model
- **Your Bar** / **Their Bar** — alternating real-time phases rather than a fully merged timeline. Their Bar would be where multi-enemy coverage/overwhelm lived, compressing all active threats into simultaneous freeform prompts.
- **Carryover** between bars would be the escalation spine — a clean Your Bar softening the next Their Bar, a rough one tightening it.
- **Per-threat musical/genre theming** would ride on Their Bar specifically, giving enemy types a readable audio identity.

### Test Music (if revisited)
- **Bosca Ceoil** (free) — simple tracker, explicit BPM field, fast clean loop export.
- **LMMS** (free) — more genre range than Bosca Ceoil's default palette.
- **AI generators (Suno/Udio)** — useful once a genre identity is decided; re-time/trim in **Audacity** afterward, since exact BPM/loop points aren't reliable from these tools directly.
- A bare metronome click at target BPM is more useful than real music for early input-timing tests.

---

## Decisions

Recorded per `dev_kit/principles/decision-ledger.md`. These unblock the first
implementation pass (see the execution plan derived from this spec); they do not resolve
the open items in Section 7 beyond what's stated below.

### Decision 1 — Vertical-slice build order

**Rationale:** The spec's own Section 8 recommends cheap prototyping before committing to
depth, and most systems (Section 7) are explicitly untuned. Building one thin, playable
loop end-to-end first (dig → simplified combat → bank resources → one fortification →
node/awakening pressure) surfaces whether the core loop is fun before any single system
is built to full depth.

**Alternatives:**

| Option | Reason Rejected |
|--------|-----------------|
| Exploration layer fully, in isolation | Delays ever seeing combat/fortification interact with digging, which is where a lot of the spec's intended tension lives (Stability strain, muster stack risk vs. reward) |
| Systems-parallel, shallow everywhere | Thin placeholders across all systems at once risks nothing being playable/coherent for longer, with no single loop to react to |
| Full spec breadth up front | Directly contradicts Section 8's own prototyping recommendation; highest risk of building depth on an unvalidated loop |

**Consequences:** The first implementation milestone is scoped to a single floor, a single
combat-hazard resolution path, and a minimal fortification/economy loop. Deeper systems
(full tactical battlefield, factions/rulers roster, industrialization, rival tunneler) are
explicitly deferred, not abandoned.

### Decision 2 — Combat hazards resolve via a numeric auto-resolve stub for the vertical slice

**Rationale:** Section 4's tactical battlefield (pre-authored NxN arena, auto-resolve +
hero control, commanders) is the single most complex system in the spec. Stubbing combat
as stats-vs-stats auto-resolve lets the exploration/economy loop (digging, muster stack,
Stability, resources, fortification) be validated fast, without the battlefield's own
unresolved questions (Section 7: hero roster, ability count, commander count) blocking
progress on everything else.

**Alternatives:**

| Option | Reason Rejected |
|--------|-----------------|
| Minimal real battlefield (small fixed grid, one enemy type, hero control) | Still requires deciding hero control scheme and at least one commander mechanic before the vertical slice can run — those are exactly the undecided items this decision defers |
| Full tactical battlefield from the start | Section 7 leaves hero roster, ability count, and commander count explicitly open; building the full system now means designing all of that first |

**Consequences:** A `combat_resolver` module returns win/loss + reward/cost from stats and
RNG only. It has no terrain, no hero-controlled actions, and no commanders. Replacing it
with the real tactical battlefield (Section 4) is planned as a distinct later milestone,
not a refactor forced by the stub's own limitations (the stub is intentionally
throwaway-shaped — a hazard's stats and outcome contract are what carry forward).

### Decision 3 — First Faction is constructed/metal-reliant + fixed home base; first Ruler is a unit-cost reducer

**Rationale:** Section 6 defines three population-sourcing axes and three base-model axes
for Faction, plus a Ruler layer on top, with the full roster and numbers explicitly left
open (Section 7). Picking the constructed/metal-reliant axis (units built directly from
extracted resources, no growth-rate mechanic) keeps the first Faction's implementation
tied to a single resource-ledger interaction rather than also requiring a population/birth
simulation. Fixed home base is used because the spec itself states this is "the default
assumption elsewhere in this spec." A cost-reduction Ruler (rather than a no-op) is chosen
specifically to validate that the Faction→Ruler layering (Ruler modifies a value Faction
exposes) works mechanically, since a no-op Ruler wouldn't exercise that seam at all.

**Alternatives:**

| Option | Reason Rejected |
|--------|-----------------|
| Growth-reliant Faction | Requires a birth/replenishment simulation at the home base before any Faction logic can be tested, which is more upfront complexity than the vertical slice needs |
| Settlement/mercenary-reliant Faction | Its core loop depends on "allied settlements found deeper," which doesn't exist yet in a single-floor vertical slice |
| Faction-selection framework with stubbed factions | More architecture than the vertical slice needs; premature given only one Faction is being built right now |
| No-op Ruler | Wouldn't exercise the Faction→Ruler modifier seam, so the layering pattern goes untested until a second Ruler is written |

**Consequences:** `faction.gd` defines the minimal base contract (`get_unit_cost()`);
`constructed_faction.gd` and `ruler.gd`/`cost_reduction_ruler.gd` are the first two
base-type-with-implementation cases in the codebase and require the shared contract-test
suite per `dev_kit/principles/solid-mechanical.md` criterion L. Growth-reliant and
settlement/mercenary-reliant Factions, the roaming/organic-spread base models, and the
rest of the Ruler roster remain open per Section 7 until a later pass.

### Decision 4 — Godot/GDScript tooling stack: GdUnit4 + gdtoolkit + pre-commit + GitHub Actions

**Rationale:** `dev_kit/README.md` states its stack-specific `ci/godot/` layer had not
been built yet; this decision is what fills it in. GdUnit4 was already the intended
choice (established outside this spec) for GDScript TDD; gdtoolkit's `gdlint`/`gdformat`
cover the `lint-clean` rubric row since GdUnit4 doesn't do linting/formatting. `pre-commit`
runs the fast checks locally; `godot-gdunit-labs/gdUnit4-action` in GitHub Actions is the
authoritative CI gate, matching `dev_kit/rubrics/run-baseline.rubrics.md`'s stated
local/CI split.

**Alternatives:**

| Option | Reason Rejected |
|--------|-----------------|
| GdUnit4's own coverage CLI flag for `coverage-*` rubric rows | No documented CLI coverage flag was found as of this writing; faking one would violate the dev_kit's own honesty convention (see `dev_kit/ci/godot/README.md`, "Not yet automated") |
| Building custom static-analysis tooling now for `ocp-shotgun-surgery` / `isp-*` / `dip-direction` | Real future work, but a GDScript call-graph/AST tool is its own project; not justified before any real source code exists |

**Consequences:** Coverage thresholds (`coverage-overall`, `coverage-changed-lines`) are
checked manually via the Godot editor's GdUnit4 inspector until a CLI coverage flag is
confirmed. `ocp-shotgun-surgery`, `isp-method-count`/`isp-stub-detection`, and
`dip-direction` are manual-review rubric rows for now, stated plainly in
`dev_kit/ci/godot/README.md` rather than covered by a placeholder script that always
passes.

### Decision 5 — Versioned release playtest artifacts, with a composite Release Readiness Score scoped to that purpose only

**Rationale:** Per-PR mechanical tracking (`dev_kit/progress-log.md`) answers "did this
change regress anything" and deliberately keeps its metrics unreduced to a single number,
per `dev_kit/principles/progress-tracking.md` Gate 1's own stated position ("does not
invent a synthetic composite score to paper over that gap"). Playtesting answers a
different question — "is this version worth a human's time to play" — for which a single
at-a-glance number alongside room for human judgement is more useful than a metrics table.
This decision introduces that number for release entries specifically, without touching
Gate 1's per-PR behaviour or contradicting its stated position there.

**Versioning scheme:** Semantic version tags (`vMAJOR.MINOR.PATCH`), computed from
Conventional Commits on every push to `main`
(`dev_kit/ci/godot/scripts/determine_version_bump.py`):
- Any commit with `!` after its type/scope, or a `BREAKING CHANGE:` footer, since the last
  tag → bump. **Pre-1.0 exception:** while `MAJOR` is `0`, a breaking change bumps
  `MINOR`, not `MAJOR` — this is semver's own "initial development" convention (anything
  may change before a `1.0.0` stability commitment), stated here so it isn't a silent
  surprise the first time it fires.
- Else any `feat:` commit since the last tag → bump `MINOR`.
- Else any `fix:` commit since the last tag → bump `PATCH`.
- Else (only `chore`/`docs`/`refactor`/`test`/`perf` since the last tag) → no bump, no
  release, no new playtest artifact. A tooling-only PR has nothing for a human to play.

**Release Readiness Score (0–100):** `60 × automated_checks_ratio + 40 × test_pass_ratio`,
computed by `dev_kit/ci/godot/scripts/release_score.py`:
- `automated_checks_ratio` — the "Automated checks passing" fraction from that release's
  `dev_kit/progress-log.md` row (e.g. `6/6` → `1.0`).
- `test_pass_ratio` — passed/total from that CI run's GdUnit4 JUnit report. **If no tests
  exist yet, this contributes `0`, not `N/A`** — a version with no tests is not "ready,"
  and the score should say so rather than hide the gap by excluding the component.
- Coverage is not in the formula: no confirmed GdUnit4 coverage CLI flag exists yet (see
  `dev_kit/ci/godot/README.md`), and this score doesn't fake a number it can't measure.

**Player-facing entry fields** (`PLAYTEST_LOG.md`, one entry per release, never filled in
by the implementing agent — same conflict-of-interest reasoning as Gate 2 generally):
Functional rating (1–5), Fun/engagement rating (1–5), a structured bug-entries table
(severity, what happened, repro steps), and freeform session/completion notes.

**Mechanism:** on a push to `main` that warrants a bump, CI tags the release, then opens a
PR (never commits to `main` directly, same as every other change in this project) adding
the `VERSION` bump and the new `PLAYTEST_LOG.md` entry, for the user to merge.

**Alternatives:**

| Option | Reason Rejected |
|--------|-----------------|
| One playtest entry per PR (the prior convention) | A tooling-only PR (most of Phase 0) has no gameplay to have an opinion about; entries should correspond to something actually playable |
| Keep individual metrics only, no composite score, for releases too | Explicitly rejected by the user in favour of a single at-a-glance readiness number for this specific purpose |
| Include coverage in the formula now | No confirmed CLI coverage flag exists yet; would require faking a number, which this project's tooling explicitly avoids elsewhere |
| CI commits the version bump / log entry directly to `main` | Would violate this project's standing rule that nothing lands on `main` without a human-reviewed PR, even from automation |

**Consequences:** `PLAYTEST_LOG.md` entries are now generated automatically per release,
not manually per PR by whichever agent implemented it — `.claude/skills/run-phase/SKILL.md`
no longer instructs appending a stub entry per phase. The very first tag this project cuts
will be `v0.1.0` (from a `feat:`-containing merge) or `v0.0.1` (from a `fix:`-only merge),
since no prior tag exists.
