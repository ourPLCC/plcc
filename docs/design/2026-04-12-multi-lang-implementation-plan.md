# PLCC v9.0.0 — High-Level Implementation Plan

**Date:** 2026-04-12
**Status:** Draft — pending review
**Companion architectural spec:** [2026-04-12-multi-lang-pipeline.md](2026-04-12-multi-lang-pipeline.md)
**Target branch:** `multi-lang` (to be created in Phase 0)
**Target release:** PLCC v9.0.0

## 1. Purpose

This document is the **roadmap** for implementing PLCC v9.0.0, not a detailed task list. It sequences the work into phases, names the strategy behind each phase, states the acceptance criteria that mark a phase as complete, and describes how phase-level design documents and detailed implementation plans are produced iteratively.

It does not contain code, TDD task steps, or exhaustive enumerations of files to touch. Those live in each phase's own implementation plan, which is written when that phase is about to begin — not now.

The companion architectural spec (`2026-04-12-multi-lang-pipeline.md`) describes *what* is being built. This document describes *how and in what order* it gets built.

## 2. Process Model

Each phase is executed through a small, full cycle of the brainstorming and planning skills. The steps of that cycle are:

1. **Phase brainstorm.** Revisit the architectural spec's relevant sections. Surface open questions specific to this phase. Resolve them through dialogue. The scope is narrow: only what this phase needs to decide.
2. **Phase design document.** Capture the decisions that emerged from the brainstorm as a short design doc dedicated to the phase. Saved to `docs/design/YYYY-MM-DD-phase-<n>-<name>.md`. This document is additive to the architectural spec, not a replacement — it fills in details the architectural spec intentionally left open.
3. **Phase implementation plan.** Produced by the writing-plans skill. A detailed TDD task list with exact files, steps, commands, and commits. Saved to `docs/plans/YYYY-MM-DD-phase-<n>-<name>.md`.
4. **Execution.** The phase plan is executed task by task, with tests at every step. Work happens on the `multi-lang` branch.
5. **Phase review.** At phase completion, a short retrospective captures what was learned, what surprised us, and whether any decisions in the architectural spec need revisiting. This feedback informs the next phase's brainstorm.

This cycle exists because implementation details for later phases cannot be honestly designed up front — they depend on what we learn from earlier phases. The architectural spec is stable; phase-level details are just-in-time.

### 2.1 The architectural spec is frozen

During v9 development, the architectural spec (`2026-04-12-multi-lang-pipeline.md`) is treated as frozen. Phase work does not edit it. If a phase reveals that an architectural decision is wrong, the response is a deliberate **architectural amendment**: a new dated section added to the spec (or a superseding spec) with a clear "amends §X because of lesson learned in Phase Y" header. This is rare and intentional. Routine phase work never touches the spec.

### 2.2 Documents produced by this plan

By the time v9.0.0 ships, the following documents exist:

- `docs/design/2026-04-12-multi-lang-pipeline.md` — architectural spec (already exists)
- `docs/design/2026-04-12-multi-lang-implementation-plan.md` — this document
- `docs/design/YYYY-MM-DD-phase-0-repo-unification.md` — Phase 0 design doc (later)
- `docs/plans/YYYY-MM-DD-phase-0-repo-unification.md` — Phase 0 detailed plan (later)
- …and similarly for Phases 1–5.

Phase-level retros are appended to each phase's design doc rather than given separate files.

## 3. v8 Support Branch Procedure

Before any v9 development begins, v8 must be preserved as a live support line so that bug fixes for existing PLCC users can continue to ship independently of v9 work.

### 3.1 Creating the `v8` branch

At the current `plcc` repository state (tip of `main` is v8.0.2), create a long-lived branch named `v8`:

```bash
cd plcc
git checkout main
git tag v8-last-main-state   # optional: name the exact commit we branched from
git checkout -b v8
git push origin v8
```

The `v8` branch is the home for:

- Bug fixes targeting existing PLCC users
- v8.0.x patch releases (v8.0.3, v8.0.4, …)
- Any security fixes that must ship while v9 is in development

The `v8` branch does *not* receive v9 work. Its only commits after this point are bug fixes. Releases from this branch continue under the v8.0.x numbering.

### 3.2 Support posture

The `v8` branch is maintained for the duration of the deprecation timeline announced alongside v9.0.0's stable release. Once v9 is stable and learning materials have migrated, a deprecation announcement names a date after which `v8` will receive security fixes only, and a later date after which `v8` is frozen (no more commits, branch preserved in read-only state).

**Freezing is not deletion.** The `v8` branch, its tags, and all of its history remain in the repository permanently, as do all commits reachable from `main` at every point in history. Nothing in this plan ever deletes git history.

### 3.3 Developer access to v8 during v9 development

A developer working on `multi-lang` who needs to run v8 locally does so by checking out the `v8` branch in a worktree:

```bash
git worktree add ../plcc-v8 v8
```

v8 is fully functional in `../plcc-v8`, with its own build system and test suite, independent of the v9 work happening in the main checkout.

This approach gives developers immediate access to v8 without requiring v8's source files to exist in the `multi-lang` working tree. The `multi-lang` tree stays focused on v9 code; v8 comparisons happen in a sibling directory.

## 4. Phase Overview

```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
 Merge    Walking    Python     Java     Polish &   Release
          skeleton   emitter    emitter  prerelease & cutover
```

Each arrow is a phase boundary. At every boundary there is a phase retro that informs the next phase's brainstorm. Phases do not overlap; each one completes and is reviewed before the next begins.

## 5. Phase 0: Repository Unification

### 5.1 Goal

Create the `multi-lang` branch on the `plcc` repository with plcc-ng's history merged in, establish the `v8` support branch, and leave `multi-lang`'s working tree with plcc-ng's code as the foundation for v9 development (no v8 files in the tree).

### 5.2 Strategy

Both repositories share a real common ancestor (`fe08748`, 2024-05-01), so a normal `git merge` produces a unified history without `--allow-unrelated-histories` or subtree tricks. 14 commits on plcc's `main` since divergence, 282 on plcc-ng's `main` — the plcc-ng side is where the bulk of v9's foundation lives.

The sequence of operations:

1. Create the `v8` support branch from current `plcc` main tip (per §3.1).
2. Add plcc-ng as a remote to the `plcc` repo and fetch its refs. Delete plcc-ng's experimental `0.0.1`–`0.0.5` tags from the local ref store before the merge so they do not pollute the unified tag namespace.
3. Create the `multi-lang` branch from current `plcc` main tip.
4. Merge `ng/main` into `multi-lang`. Resolve conflicts on overlapping files (README, LICENSE, devcontainer, `.gitignore`, etc.) according to the conflict policy set during the Phase 0 brainstorm — this plan does not pre-decide which side wins for which file. The merge commit preserves both lineages' history.
5. Immediately after the merge commit, a follow-up commit removes v8's source files from the `multi-lang` working tree. The files remain accessible via the `v8` branch and via history; they simply no longer appear at `multi-lang`'s tip.
6. Verify CI builds green on the new `multi-lang` tip. plcc-ng's existing test suite is the relevant signal here — it's what's running on `multi-lang` right now.
7. Push `multi-lang` and `v8` to the remote.

### 5.3 Acceptance criteria

- `v8` branch exists on the remote and is bootable — `git checkout v8 && <v8's existing test command>` works.
- `multi-lang` branch exists on the remote.
- `git log multi-lang` shows commits from both the plcc lineage and the plcc-ng lineage, joined by a single merge commit.
- plcc-ng's existing test suite passes on `multi-lang`'s tip.
- `multi-lang`'s working tree contains plcc-ng's Python code and no v8 source files.
- plcc-ng's experimental `0.0.x` tags are not present in the remote's tag namespace.

### 5.4 Out of scope for Phase 0

- Any refactoring of plcc-ng's internal structure (that's Phase 1).
- Any new primitives, plugins, or architecture work (that's Phase 1).
- Renaming files or packages (that's Phase 1 or later as needed).
- Publishing to PyPI (that's Phase 4).

### 5.5 Phase 0 design document scope

The phase design doc will decide: exactly which v8 files to remove in the working-tree-cleanup commit, how to resolve the specific conflict set (README, LICENSE, etc.), whether the merge uses `--no-ff` or fast-forward semantics, the exact remote URL and credentials used to fetch plcc-ng, and the tag cleanup procedure. None of that is decided here.

## 6. Phase 1: Walking Skeleton

### 6.1 Goal

Build a thin, end-to-end pipeline that drives a trivial grammar file all the way through to a rendered PlantUML class diagram, proving every JSON contract and the plugin discovery mechanism in one pass.

### 6.2 Strategy

This is a **walking skeleton** in the Alistair Cockburn sense: every part of the pipeline exists but is only as thick as it needs to be to process a minimal grammar. The value is not in what the skeleton can do (very little) but in what its existence proves (every contract is honored, every boundary is crossed, the plugin discovery works).

Five Level 0 primitives get stubs:

- `plcc-spec` — wrap plcc-ng's existing spec parser; emit spec JSON
- `plcc-tokens` — wrap plcc-ng's existing scanner; emit token JSONL
- `plcc-tree` — hand-rolled minimum viable parser, enough to handle the trivial grammar
- `plcc-model` — minimal spec → model transform, enough to describe the trivial grammar's class hierarchy
- `plcc-emit` — dispatcher that discovers plugins via `importlib.metadata.entry_points(group="plcc.emitters")`

One emitter plugin gets built:

- `plcc-emit-plantuml` — smallest possible emitter. Reads model JSON, writes a `.puml` file. No `build()` hook. No runtime library. Declares itself under the `plcc.emitters` entry-point group.

One Level 2 command gets built:

- `plcc-make` — orchestrates the phase sequence in §9 of the architectural spec. Cleans `build/`, runs the pipeline, calls the plugin.

The trivial grammar is chosen to exercise the shape of every contract without needing any feature richness. Something like a grammar for a single expression language with one lexical rule, one syntactic rule, and one semantic section emitting PlantUML.

### 6.3 Why PlantUML first

PlantUML is the simplest possible emitter plugin. It has no runtime library, no build step, and its output is a single text file that can be visually verified by rendering it in a browser or local tool. It proves the plugin discovery mechanism, the `emit()` contract, and the end-to-end pipeline without the complexity of a runnable interpreter. It is "hello world" for the plugin system.

### 6.4 Acceptance criteria

- `plcc-make trivial.plcc` produces `build/spec.json`, `build/model.json`, and `build/diagram/<something>.puml`.
- Running the generated `.puml` through PlantUML renders a valid class diagram.
- The diagram correctly represents the trivial grammar's class hierarchy (manually verified).
- `plcc-emit-plantuml` is discovered via the plugin mechanism, not hardcoded.
- `plcc-make -h` describes the tool correctly.
- CI on `multi-lang` runs the skeleton end-to-end against the trivial grammar and asserts the expected output exists.

### 6.5 Explicitly deferred to later phases

- Handling any grammar more complex than the trivial one (Phases 2, 3)
- Runnable interpreters (Phase 2)
- Backwards compatibility with v8 grammars (Phase 3)
- Error records and error rendering (Phase 2 at the earliest)
- `plcc-scan`, `plcc-parse`, `plcc-rep` orchestrators (Phase 4)
- PyPI publication (Phase 4)

### 6.6 Phase 1 design document scope

The phase design doc will decide: the exact shape of the trivial grammar; the exact JSON schemas for spec, token, tree, and model (minimum viable versions); the internal module layout within the `plcc` package for the Level 0 primitives; how `pyproject.toml` declares console scripts and the `plcc.emitters` entry-point group; the plugin package's directory layout; how `plcc-make` locates the grammar file and `build/` directory relative to the current working directory; and the testing strategy for the skeleton (unit tests per primitive plus an end-to-end smoke test).

## 7. Phase 2: Python Emitter Thickening

### 7.1 Goal

Grow the skeleton into a pipeline that produces a runnable Python interpreter for a simple arithmetic grammar. `plcc-rep` lands in this phase, and the first interactive REPL session becomes possible.

### 7.2 Strategy

This phase is where the code model earns its keep as a retargeting pivot. The Python emitter is the first emitter that produces code capable of actually running, which means the model must describe enough structure for an emitter to generate:

- Class definitions with inheritance
- Constructors with field initialization
- Method slots with opaque semantic bodies
- Token references and tree-walking
- A top-level entry point that drives the parse → evaluate loop

The parser runtime (`plcc-tree`) thickens from hand-rolled to a real LL(1) parser table driver, consuming the grammar structure that plcc-ng has already validated. `plcc-model` thickens to describe a realistic class hierarchy instead of the trivial skeleton. `plcc-emit-python` gets built out with templates, a bundled runtime library, and enough emission logic to handle the simple arithmetic grammar end-to-end. `plcc-rep` orchestrates the runtime pipeline and handles tty prompting.

Error records (§8 of the architectural spec) are introduced in this phase because the REPL needs them: a malformed program in the REPL must produce an error record that the interpreter renders without tearing down the pipeline.

The test grammar for this phase is a simple expression-evaluator language: numeric literals, addition, subtraction, multiplication, division, parenthesization. Enough to have a real tree, real semantic methods, real evaluation, and a meaningful REPL interaction.

### 7.3 Why Python before Java

Per the architectural spec §17 (open risks): the code model is the retargeting pivot, and building Python before Java forces the model to be language-neutral by construction. If Java were built first, the model would quietly accumulate Java-isms that only surface when a second target is attempted. Python is the stress test that prevents that accumulation.

### 7.4 Acceptance criteria

- `plcc-make arith.plcc` produces `build/py/` containing a runnable Python interpreter for the test grammar.
- The generated Python interpreter includes the bundled `runtime/` directory (per spec §9).
- `plcc-rep arith.plcc` starts a REPL. Typing `1 + 2 * 3` produces `7`. Typing a malformed expression produces an error message and the REPL continues.
- `plcc-rep arith.plcc program.txt` evaluates the program and exits.
- `cd build/py && python main.py < program.txt` works as a way to invoke the generated interpreter without `plcc-rep`.
- Error records flow through the pipeline as in-band JSON; they are never confused with tool failures (which still use stderr and nonzero exit codes).
- `plcc-tree` is a real parser, not a hand-rolled stub.
- `plcc-model` describes the test grammar's class hierarchy accurately enough for Python emission.

### 7.5 Explicitly deferred to later phases

- Java emission (Phase 3)
- Passing the `languages` backwards-compat test suite (Phase 3)
- `plcc-scan` and `plcc-parse` visualizer commands (Phase 4)
- PyPI publication (Phase 4)

### 7.6 Phase 2 design document scope

The phase design doc will decide: the exact shape of the code model JSON beyond the skeleton (inheritance, method slots, semantic blocks, type representation); the LL(1) parser table format and runtime algorithm; the template strategy for Python code emission (Jinja, string templates, or ad-hoc construction); the layout and content of the bundled Python runtime library; the error record schema; the `plcc-rep` tty detection and prompting behavior; the test grammar's exact shape; and the test strategy for generated interpreter correctness.

## 8. Phase 3: Java Emitter and Backwards Compatibility

### 8.1 Goal

Port v8's Java generation logic into a `plcc-emit-java` plugin, and iterate until the `languages` test repository's full suite passes in CI against `multi-lang`.

### 8.2 Strategy

This is the phase that makes v9 a drop-in replacement for v8 for existing users. By this point, the code model is stable (Phase 2 stress-tested it), `plcc-make` works end-to-end (Phase 1), and the plugin contract is proven (Phase 1). What's new in this phase is:

- A `plcc-emit-java` plugin package with emission logic ported from v8's Java generator
- A bundled Java runtime library inside the plugin, distilled from v8's runtime support classes
- A `build()` hook on the Java emitter that runs `javac`
- Whatever additions to the code model are needed to describe language constructs that v8 grammars use but the Python test grammar did not
- CI integration for the `languages` test suite as a continuous backwards-compat signal

The port is not a rewrite of v8's Java generator. Wherever possible, v8's existing logic is adapted rather than reinvented — the goal is semantic equivalence of output, not improvement. Any improvement happens only when v8's approach cannot be expressed as a code-model-consuming emitter without Java-isms leaking upward.

The `languages` suite runs continuously throughout the phase. It starts red (the Java emitter doesn't exist at phase start) and iteratively turns green grammar by grammar as the emitter handles more features. A phase progress board tracks which of the `languages` grammars have passed.

### 8.3 The red CI bet

This phase is where the strategic bet from Axis 2 pays off — or costs us. The `languages` CI job has been red since the start of v9 development, and only now does it turn green. The bet is that a code model stress-tested by Python before Java is more language-neutral than one that was Java-first, and therefore the port goes faster than it would have without Phase 2's pressure.

If the bet is wrong and the code model turns out to be Python-biased instead of language-neutral, this phase will reveal it, and the response will be an architectural amendment per §2.1 followed by rework. The phase retro is especially important here.

### 8.4 Acceptance criteria

- `plcc-emit-java` plugin exists, is installed as a dependency of `plcc`, and is discovered via the `plcc.emitters` entry-point group.
- `plcc-make <grammar>` for any grammar in the `languages` repo produces working Java code in `build/Java/` with a compiled class hierarchy after the emitter's `build()` hook runs.
- The full `languages` test suite passes in CI on `multi-lang`.
- The Java runtime library is bundled inside the `plcc-emit-java` plugin package per spec §10.2.
- Semantic compatibility (spec §14) is achieved: generated Java may differ from v8's output in names and layout, but runtime behavior is equivalent as measured by the `languages` suite.

### 8.5 Explicitly deferred to later phases

- `plcc-scan` and `plcc-parse` visualizer commands (Phase 4)
- PyPI publication (Phase 4)
- Learning materials updates (Phase 5)
- Cutover to `main` (Phase 5)

### 8.6 Phase 3 design document scope

The phase design doc will decide: the exact mapping from v8's code generator to the `emit()` callable; the bundled Java runtime library's content and internal API; the `javac` invocation strategy for the `build()` hook; the CI configuration that runs the `languages` suite against `multi-lang`; the strategy for handling any grammar in `languages` that reveals a code model gap (architectural amendment vs. emitter workaround); and the process for tracking phase progress against the full grammar list.

## 9. Phase 4: Polish and Prerelease

### 9.1 Goal

Finish the pedagogical visualizer commands (`plcc-scan`, `plcc-parse`), ready the package for PyPI, and publish `plcc==9.0.0a1` as the first prerelease for early adopters.

### 9.2 Strategy

By the start of this phase, the hard architectural work is done: the pipeline runs end-to-end, both Python and Java emitters work, and the `languages` suite is green. What remains is user-facing polish and the plumbing to get v9 into pip users' hands.

`plcc-scan` and `plcc-parse` are the visualizer commands that let students watch the pipeline's intermediate outputs: tokens and parse trees in human-readable form. They reuse the Level 0 primitives directly, format the output for terminals, and handle the same file+stdin input model as `plcc-rep`. They are small additions on top of infrastructure that already exists.

PyPI publication requires `pyproject.toml` polish: correct metadata, classifiers, console-script entry points for every Level 0 and Level 2 command, the `plcc.emitters` entry-point group declaration (populated from built-in emitter modules inside the `plcc` package), README rendering on PyPI, and a release workflow.

**Built-in emitter packaging decision:** the three built-in emitters (Java, Python, PlantUML) are bundled inside the `plcc` package itself for v9.0.0, not published as separate PyPI packages. They live as submodules (e.g. `plcc.emit.java`, `plcc.emit.python`, `plcc.emit.plantuml`) and register themselves under the `plcc.emitters` entry-point group from within `plcc`'s own `pyproject.toml`. A plain `pip install plcc` installs all three. If there is later demand to extract them into separate `plcc-emit-<lang>` PyPI packages, that extraction can happen in a future release without breaking the plugin contract — third-party emitters already have a proven path via the entry-point mechanism.

The first prerelease is tagged `9.0.0a1` and published. The prerelease tag signals that v9 is not yet considered stable and that API changes are possible. Early adopters install with `pip install --pre plcc` and provide feedback.

### 9.3 Acceptance criteria

- `plcc-scan <grammar> <program>` prints the token stream in a human-readable format.
- `plcc-parse <grammar> <program>` prints the parse tree in a human-readable format.
- Both visualizer commands handle file and stdin input per spec §6.
- `pip install plcc` on a fresh environment (Linux, macOS, Windows) installs v9 and all three built-in emitters with no additional steps.
- `plcc-make --help` (and every other Level 2 command's `--help`) produces useful output.
- `plcc==9.0.0a1` is published to PyPI.
- The `languages` suite still passes after the packaging polish (no regressions from entry-point restructuring).

### 9.4 Explicitly deferred to later phases

- Stable 9.0.0 release (Phase 5)
- `multi-lang → main` cutover (Phase 5)
- Learning materials updates (Phase 5)
- Deprecation timeline for v8 (Phase 5)

### 9.5 Phase 4 design document scope

The phase design doc will decide: the exact terminal output format for `plcc-scan` and `plcc-parse`; how they present error records from the pipeline; the full `pyproject.toml` layout; the release workflow and publishing credentials; the GitHub Actions or equivalent CI configuration for tagged releases; whether built-in emitters are installed as true dependencies or as part of the `plcc` package itself.

## 10. Phase 5: Release and Cutover

### 10.1 Goal

Iterate on prereleases based on early-adopter feedback, coordinate the update of learning materials, publish `plcc==9.0.0` stable, and merge `multi-lang` into `main` as v9 becomes the canonical PLCC.

### 10.2 Strategy

Phase 5 is the least mechanical of the phases. It is about iteration, coordination, and cutover timing. The work is:

- **Prerelease iteration.** Additional alphas (`9.0.0a2`, `9.0.0a3`, …) and betas (`9.0.0b1`, …) respond to feedback from the two pilot faculty. Each prerelease is cut from `multi-lang` with a version bump and a PyPI publish.
- **Pilot evaluation with the two faculty users.** The known PLCC user population consists of two faculty: the project maintainer and one colleague who meets with the maintainer weekly. Prereleases are evaluated through those weekly conversations and any ad-hoc testing either faculty chooses to do against their own course materials. The exact test cadence and criteria are decided during the Phase 5 brainstorm — which may be as informal as "does it work for the next semester's course?" — but the small user population means pilot testing is a deliberate conversation, not a public beta program.
- **Learning materials update.** The parallel effort to update course materials, example grammars, and documentation to match v9's commands and output. The maintainer owns this directly (answering spec §17's open question about maintainer identity). The cutover is gated on this work being sufficiently complete for at least one of the two faculty's courses.
- **Deprecation timeline.** A public announcement names the dates on which (a) v8 transitions to security-fix-only support, (b) v8 is frozen. These dates give existing users a known runway.
- **Cutover.** Tag `main` with `v8-final`. Merge `multi-lang` into `main` (normal git merge, possibly through a review PR). Publish `plcc==9.0.0` stable to PyPI from the merged `main`. Archive the `plcc-ng` repository with a README pointing to the unified history in `plcc`.

### 10.3 Acceptance criteria

- At least one of the two pilot faculty has run v9 against their own course workflow (or an approximation of it) and reported no blocking issues.
- Learning materials are updated to match v9 commands and behavior.
- `v8-final` tag exists on `main`'s pre-cutover tip.
- `multi-lang` has been merged into `main`.
- `plcc==9.0.0` is published to PyPI as a stable release.
- `plcc-ng` repository is archived with a README pointing to `plcc`.
- A deprecation timeline for v8 has been published in a public location.

### 10.4 Phase 5 design document scope

The phase design doc will decide: the exact sequence of prerelease versions; the pilot user list and feedback collection mechanism; the learning materials update checklist; the deprecation timeline dates; the cutover procedure (PR-reviewed merge vs direct merge); the exact wording of the deprecation announcement; and the `plcc-ng` archive README content.

## 11. Cross-Phase Concerns

### 11.1 TDD discipline

Every primitive, every plugin, and every orchestrator is built test-first. plcc-ng already uses TDD; the existing test suite is the starting point and is extended, not replaced. The writing-plans skill's task granularity (write failing test → run to confirm failure → write minimal code → run to confirm pass → commit) applies to every task in every phase-level plan.

### 11.2 CI strategy

CI runs on every push to `multi-lang` throughout development. The CI job set grows phase by phase:

- **After Phase 0:** plcc-ng's existing tests run against `multi-lang`.
- **After Phase 1:** the skeleton smoke test (trivial grammar → PlantUML) is added.
- **During Phase 2:** Python emitter tests and the REPL integration tests are added.
- **During Phase 3:** the `languages` suite is added and runs continuously — starting red and turning green grammar by grammar.
- **Phase 4:** packaging smoke test (install from built wheel and run a smoke test grammar).
- **Phase 5:** release workflow testing on prerelease tags.

Tests that are expected to be red (the `languages` suite during Phase 3 before grammars are ported) are marked as such in CI so the overall pipeline status remains meaningful. They flip to required once their grammar passes locally.

### 11.3 Prerelease cadence

Prereleases are cut from `multi-lang` at natural milestones:

- `9.0.0a1` — at the end of Phase 4 (first PyPI publication; pipeline complete through Java and packaged)
- `9.0.0a2`, `a3`, … — during Phase 5 as iteration warrants
- `9.0.0b1` — when most known issues are addressed and the release is feature-complete
- `9.0.0rc1` — when ready for stable release, pending final learning materials sync
- `9.0.0` — the stable release, published from `main` after the cutover merge

Nothing before Phase 4 is published. Earlier phases don't produce usable artifacts for end users.

### 11.4 Phase retros feeding back into the architectural spec

Section 2.1 notes that architectural amendments to the spec are rare and intentional. When a phase retro surfaces a decision that needs to be amended, the amendment takes the form of a new dated section appended to `2026-04-12-multi-lang-pipeline.md`, clearly labeled "Amendment from Phase N retro: …". The original sections are not edited. This keeps the history of architectural thinking visible and preserves the context in which later decisions were made.

Routine phase learnings (things that worked, things that didn't, surprises that didn't warrant spec changes) are captured in each phase design doc's retro section, not the architectural spec.

### 11.5 Working in the plcc-ng subdirectory during Phase 0

The current `plcc` working directory already contains a `plcc-ng/` subdirectory that is itself a clone of the plcc-ng repository (discovered during Phase 0 git reconnaissance). This subdirectory was used to inspect plcc-ng's state during brainstorming. It must not be confused with the merge operation: the Phase 0 merge uses plcc-ng as a git *remote*, not as a directory copy. The `plcc-ng/` subdirectory should be removed or ignored before the merge begins, and is not committed to `multi-lang` in any phase.

## 12. What Each Phase Owes the Next

Each phase leaves behind artifacts that the next phase builds on. Enumerating those artifacts explicitly helps surface design debt (when a phase accepts an artifact that isn't ready) and helps each phase brainstorm start with a clear picture of what's already fixed.

**Phase 0 → Phase 1:**
- `multi-lang` branch with plcc-ng's Python code as the foundation
- plcc-ng's existing test suite passing
- Known location for v9 source code (plcc-ng's existing package layout; the Phase 1 design doc decides whether to reorganize it)
- `v8` support branch available for comparison

**Phase 1 → Phase 2:**
- All five Level 0 primitives exist as console-script entry points
- Minimum viable JSON schemas for spec, token, tree, model are defined
- Plugin discovery mechanism works
- `plcc-make` orchestrator works
- End-to-end CI smoke test exists and is green
- A known-working trivial grammar and its expected `build/` output

**Phase 2 → Phase 3:**
- Code model is rich enough to describe a realistic class hierarchy (inheritance, method slots, semantic blocks, type representation)
- `plcc-tree` is a real LL(1) parser runtime
- `plcc-rep` orchestrator works end-to-end
- Error record schema is defined and flowing in-band
- Python emitter provides a working reference for what an emitter plugin looks like in practice
- Bundled runtime library pattern is established

**Phase 3 → Phase 4:**
- Java emitter plugin works
- `languages` test suite passes in CI
- Code model is stable across two target languages (no more expected churn)
- A known-good baseline for backwards compatibility

**Phase 4 → Phase 5:**
- Pipeline is installable via `pip install --pre plcc` on every supported OS
- `plcc-scan` and `plcc-parse` visualizers work
- First prerelease is published and at least internally validated
- Release workflow exists and is repeatable

**Phase 5 → post-release:**
- v9.0.0 stable on PyPI
- `main` is v9
- `v8` branch is the support line with a published deprecation timeline
- Learning materials match v9
- `plcc-ng` repository archived with a pointer to the unified history

## 13. What This Plan Does Not Decide

- Exact file paths, module names, or class hierarchies inside `plcc` core (Phase 1 design doc)
- The exact schema of any JSON format (Phase 1 and Phase 2 design docs)
- The LL(1) parser algorithm and runtime (Phase 2 design doc)
- How semantic `%%%` blocks are lexed and attached to methods (Phase 2 design doc)
- The emitter template strategy for any language (per-phase design docs)
- The bundled runtime library's internal API for any language (per-phase design docs)
- The error record schema (Phase 2 design doc)
- The `languages` suite integration mechanics (Phase 3 design doc)
- The PyPI release workflow mechanics (Phase 4 design doc)
- The exact deprecation timeline dates (Phase 5 design doc)

These are deliberately deferred. Forcing them now would either produce speculative designs that don't survive first contact with the code or lock in choices before we've earned the right to make them.

## 14. Open Questions for Review

- **Phase 3 red CI duration.** The `languages` CI job is expected to be red for the entire Phase 3 duration. Is that acceptable, or does it warrant a separate CI configuration until it turns green?
- **Maintainer capacity.** This plan assumes single-developer bandwidth with AI assistance. If additional maintainers join any phase, their onboarding is the responsibility of the phase-level design doc, not this roadmap.

### 14.1 Questions resolved during roadmap review

- **Phase 0 merge conflict resolution policy.** Resolved: the conflict policy is decided during the Phase 0 brainstorm, not pre-decided in this roadmap. §5.2 now reflects this.
- **Phase 4 built-in emitter packaging.** Resolved: the three built-in emitters (Java, Python, PlantUML) are bundled inside the `plcc` package itself for v9.0.0. They live as submodules and register under the `plcc.emitters` entry-point group from `plcc`'s own `pyproject.toml`. Extraction into separate `plcc-emit-<lang>` packages can happen in a future release if demand emerges. §9.2 captures this.
- **Phase 5 pilot user identification.** Resolved: the known PLCC user population is the maintainer and one colleague who meets with the maintainer weekly. Pilot evaluation happens through that existing conversation cadence; the exact mechanics are decided during the Phase 5 brainstorm. §10.2 captures this.
