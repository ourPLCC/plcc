# PLCC Multi-Language Pipeline Architecture

**Date:** 2026-04-12
**Status:** Draft — pending review
**Target release:** PLCC v9.0.0
**Branch:** `multi-lang` (to be created)

## 1. Goal

Make PLCC adoptable by faculty whose students do not know Java, by refactoring PLCC into a Unix-style pipeline of small JSON-filter tools and a plugin-based code generator that can emit interpreters in multiple target languages.

## 2. Non-Goals

- Replacing or competing with production compiler toolchains. Generated interpreters are pedagogical artifacts, not production software.
- Supporting non-OO target languages. Retargeting is limited to modern OO languages because the pedagogy depends on class hierarchy and polymorphic dispatch.
- Pluggable scanners, parsers, or verifiers. Only emitters are pluggable in v9. Verifiers may become pluggable in a later version if demand emerges.
- Bit-exact compatibility with v8's generated Java output. See §13.
- Windows-native shell pipelines. Cross-platform support comes from Python orchestration, not from shell portability. See §6.

## 3. Motivation and Context

PLCC is an educational compiler-compiler used to teach programming language concepts. As of v8.0.2 it generates only Java, which limits adoption to courses and institutions where students already know Java. Faculty at institutions that teach Python, TypeScript, or other languages as their primary language cannot adopt PLCC without imposing a language-learning burden on their students.

A parallel project, `plcc-ng`, is a clean-room rewrite in Python by students using TDD. It has completed spec parsing (lexical, syntactic, and semantic sections), a working scanner, LL(1) validation, and CLIs for `spec` and `scan`. It has not built the parser runtime or code generator. plcc-ng shares a common git ancestor with plcc and contains 282 commits of student work since divergence.

This design builds on plcc-ng's foundation rather than starting over, preserves student contributions from both lineages in a unified git history, and refactors the result into a pipeline architecture that supports multiple target languages through a plugin system.

## 4. Architecture Overview

PLCC v9 is a pipeline of small tools communicating through JSON. The pipeline has two layers:

- **Level 0** primitives are single-responsibility JSON filters. Each reads a specific JSON format on stdin (or a file path argument) and writes a specific JSON format on stdout. Primitives are composable by hand on a Unix command line.
- **Level 2** user-facing commands are Python orchestrators that compose Level 0 primitives into pipelines using `subprocess.Popen`. They match the vocabulary of existing PLCC learning materials.

Level 1 (intermediate compositions) is deliberately unoccupied in v9. It may emerge later if pedagogical use cases justify it.

```
                     ┌──────────────────────────────────────────────┐
                     │                 Level 2                      │
                     │  plcc-make   plcc-scan   plcc-parse  plcc-rep│
                     └───────────────────┬──────────────────────────┘
                                         │ orchestrates
                                         ▼
         ┌────────────┬──────────────┬──────────┬──────────────┬─────────┐
         │ plcc-spec  │ plcc-tokens  │ plcc-tree│ plcc-model   │plcc-emit│
         │            │              │          │              │         │
         │ grammar    │ text stream  │ tokens   │ spec JSON    │ model   │
         │   ↓        │   ↓          │   ↓      │   ↓          │   ↓     │
         │ spec JSON  │ token JSONL  │ tree JSON│ code model   │ source  │
         │            │              │          │              │ files   │
         └────────────┴──────────────┴──────────┴──────────────┴─────────┘
                                                                   │
                                                                   ▼
                                                  ┌──────────────────────────┐
                                                  │  Emitter plugin registry │
                                                  │  plcc.emitters entry pts │
                                                  └──────────────────────────┘
```

## 5. Level 0 Primitives

Each primitive is a pip console-script entry point provided by the `plcc` package. All are pure JSON filters except `plcc-emit`, which writes files to disk.

| Command | Input | Output | Role |
|---|---|---|---|
| `plcc-spec` | grammar file path | spec JSON (stdout) | Parse a `.plcc` grammar file into a structured spec. Already exists in plcc-ng as `spec`; renamed for namespace hygiene. |
| `plcc-tokens` | text stream (stdin) + spec JSON path | token JSONL (stdout) | Tokenize a character stream into a line-delimited JSON stream of tokens. Stateless; runs until EOF. |
| `plcc-tree` | token JSONL (stdin) + spec JSON path | tree JSON (stdout) | Parse tokens into an abstract syntax tree. Knows program boundaries from the grammar's start symbol. Long-running; emits one tree per completed program. |
| `plcc-model` | spec JSON (stdin or path) | code model JSON (stdout) | Transform a language spec into a language-neutral OO code model: classes, inheritance, attributes, constructors, method slots, and opaque semantic blocks. |
| `plcc-emit` | code model JSON (stdin or path) + `--target=<lang>` + `--output=<dir>` | source files in `<dir>` | Dispatch to an emitter plugin. The plugin writes generated source files and copies its bundled runtime into `<dir>`. The only primitive with side effects other than stdout. |

Naming rationale: the four pure filters (`spec`, `tokens`, `tree`, `model`) are named after their output. `emit` is a verb because it is the one primitive that writes files — the asymmetry is a signal, not a bug. `tree` is preferred over `ast` because it is approachable without jargon; `tokens` is preferred over `lex` or `tokenize` because it is a noun and matches the output. `model` is preferred over `code-model` for brevity and because `plcc-code` would be confusable with `plcc-emit`.

## 6. Level 2 Commands

Level 2 commands are Python modules published as pip console-script entry points. They orchestrate Level 0 primitives using `subprocess.Popen`, wire stdin/stdout between stages, handle tty detection and prompting, and present errors to the user.

| Command | Role | Replaces |
|---|---|---|
| `plcc-make` | Build the project from a grammar file. Always cleans `build/` before rebuilding. See §9 for phase sequence. | `plccmk` |
| `plcc-scan` | Pedagogical scanner view. Reads source input, runs it through `plcc-tokens`, prints tokens in a human-readable format. | `scan` |
| `plcc-parse` | Pedagogical parser view. Reads source input, runs it through `plcc-tokens` then `plcc-tree`, prints parse trees in a human-readable format. | (new; previously part of `rep`) |
| `plcc-rep` | REPL. Reads source input (files then stdin if interactive), runs it through `plcc-tokens` then `plcc-tree` then the interpreter, prints evaluation results. Handles prompting in tty mode. | `rep` |

All Level 2 commands take the same input model: zero or more file arguments followed by stdin. Files are concatenated in order, then stdin is appended. In interactive mode (`sys.stdin.isatty()`), the orchestrator emits prompts to stderr before each read.

**No shell dependency.** Layer 2 orchestrators do not invoke `cat`, `sh`, or any external shell. They open files through `pathlib`, read stdin through `sys.stdin`, and write bytes to the first subprocess's stdin pipe. This works identically on Linux, macOS, and Windows without platform branching.

Students or instructors who want to run the primitives by hand from a Unix shell can do so. That usage is documented as a teaching aid but is not the path any installed Level 2 command takes.

## 7. JSON Contracts

This section describes the shape of data flowing between stages at a high level. Exact schemas are the implementation plan's responsibility; this spec establishes only the contract and the error-record discipline.

### 7.1 Spec JSON

Output of `plcc-spec`. Contains lexical rules, syntactic rules, semantic sections (one per `% <tool> <language>` divider), and metadata needed by downstream primitives. Already produced by plcc-ng's existing `spec` command; the shape of the v9 spec JSON starts from whatever plcc-ng emits today and is refined as downstream primitives require.

### 7.2 Token JSONL

Output of `plcc-tokens`. One JSON object per line, each describing a single token: kind, lexeme, source position. A final line marks end-of-stream. Error tokens are in-band records per §8.

### 7.3 Tree JSON

Output of `plcc-tree`. One JSON object per completed program, each describing an abstract syntax tree rooted at the grammar's start symbol. Long-running: `plcc-tree` emits one tree and resumes reading tokens for the next program.

### 7.4 Code Model JSON

Output of `plcc-model`. A language-neutral description of the OO class hierarchy that an emitter will realize in its target language:

- **Classes** with inheritance relationships
- **Attributes** with types described abstractly (primitive, reference, optional, list-of)
- **Constructors** with parameter lists and field bindings
- **Method slots** — named methods with parameter lists and opaque bodies
- **Semantic blocks** — opaque strings carrying target-language code from the grammar's `%%%` sections, tagged with the source language

The code model is the retargeting pivot. Every emitter consumes this format; adding a new target language means writing an emitter that reads code model JSON and produces source files. The code model does not know anything about any specific target language.

### 7.5 Error Records

See §8.

## 8. Error Handling

Errors travel through the pipeline as in-band JSON records. Every JSON filter in the pipeline knows how to recognize, pass through, and (where appropriate) emit a record of the form:

```json
{ "kind": "error", "stage": "plcc-tree", "severity": "error",
  "message": "expected ';' after expression", "source": { ... } }
```

Downstream stages pass error records through unchanged unless they consume them (e.g. an interpreter renders the error to the user and resumes reading the next program). This keeps the REPL robust by construction: a single malformed program produces an error record, the interpreter prints it, and the pipeline continues serving subsequent programs. No stage restarts, no pipe teardown.

`stderr` and nonzero exit codes are reserved for **tool failures**, not input errors. A missing spec file, an internal bug, an I/O error, or a plugin-discovery failure writes to stderr and exits nonzero. A syntax error in a student's program is an in-band error record and does not affect exit status.

## 9. Build Output Layout

`plcc-make` produces all generated artifacts under a single top-level `build/` directory:

```
build/
├── spec.json           # output of plcc-spec
├── code-model.json     # output of plcc-model
├── Java/               # output of plcc-emit for the first semantic section
│   ├── <generated .java files>
│   └── plcc_runtime/   # runtime library copied from the Java emitter plugin
├── py/                 # output of plcc-emit for a second semantic section
│   ├── <generated .py files>
│   └── plcc_runtime/   # runtime library copied from the Python emitter plugin
└── ...
```

Key properties:

- **Single directory to clean.** `plcc-make` always runs `rm -rf build/` before rebuilding. There is no `-c` flag in v9; clean-and-rebuild is the default and only behavior. (A future option to skip cleaning can be added if a concrete need arises.)
- **Single `.gitignore` line.** `build/` in the project's `.gitignore` excludes every generated artifact.
- **Intermediate files are visible.** `spec.json` and `code-model.json` live at the top of `build/` where students can `cat` them. This supports the pedagogy: the pipeline is inspectable, not magical.
- **One output subdirectory per semantic section.** Each `% <tool> <language>` divider in the grammar produces one subdirectory named `<tool>`, emitted by the plugin for `<language>`.
- **Generated output is disposable.** Students are expected to regenerate frequently. Source (the grammar file) is what persists; `build/` is ephemeral.

`plcc-make` phase sequence:

1. **Clean:** `rm -rf build/`
2. **Spec:** `plcc-spec grammar > build/spec.json`
3. **Model:** `plcc-model build/spec.json > build/code-model.json`
4. **Emit:** for each semantic section, look up the emitter plugin for that section's language, call `emit()` to produce files in `build/<tool>/`, and copy the plugin's bundled runtime into `build/<tool>/plcc_runtime/`.
5. **Build:** for each semantic section, if the emitter plugin defines a `build()` hook, call it to compile or prepare the emitted code (e.g. run `javac` for Java).

If any phase fails, `plcc-make` reports the error and stops; subsequent phases do not run.

## 10. Emitter Plugin System

Emitters are discovered at runtime through Python's `importlib.metadata` entry-point mechanism. The `plcc` package declares a plugin group `plcc.emitters`. Each emitter package registers itself under that group.

### 10.1 Plugin Contract

An emitter plugin is a Python package exposing two callables:

```python
def emit(code_model: dict, options: dict) -> dict[str, str]:
    """
    Transform a code model into target-language source files.

    Returns a mapping of {relative_path: file_contents}.
    The caller writes these files into the output directory.
    """

def build(output_dir: Path, options: dict) -> None:
    """
    Optional. Compile or prepare the emitted code.
    Called after files are written and the runtime is copied in.
    Omit this function if the target language needs no build step.
    """
```

`options` carries presentation flags such as `--semantics=hide|note|comment|body`, which control how semantic `%%%` blocks appear in the emitted output. PlantUML and similar diagram emitters use `--semantics=note` or `--semantics=hide`; interpreter emitters use `--semantics=body`.

### 10.2 Plugin Package Layout

Each emitter plugin package bundles its own runtime library. A reference layout:

```
plcc_emit_python/
├── __init__.py          # defines emit() and optionally build()
├── templates/           # generation templates (Jinja or equivalent)
└── runtime/             # copied verbatim into build/<tool>/plcc_runtime/
    ├── __init__.py
    ├── token.py
    ├── node.py
    └── parser.py
```

The runtime lives inside the plugin so that:

- **Plugin authors own their runtime.** A plugin for a new language defines both the generated code shape and the base classes those generated classes inherit from. No coordination with plcc core required.
- **Output is self-contained.** A student running `cd build/py && python main.py` needs nothing beyond their target language's interpreter. No `plcc_runtime` PyPI dependency, no Maven Central lookup, no crates.io.
- **One install per language.** `pip install plcc-emit-rust` brings in emission logic, templates, and runtime in a single unit. Runtime bugs are fixed by releasing a new version of the plugin package.
- **Regeneration is cheap.** Students regenerate frequently (source is what persists, `build/` is disposable), so "runtime is copied into every rebuild" is not a cost.

### 10.3 Discovery

`plcc-emit --target=<lang>` loads emitters via:

```python
from importlib.metadata import entry_points
for ep in entry_points(group="plcc.emitters"):
    if ep.name == target_lang:
        emitter = ep.load()
```

If no plugin is found for a requested target, `plcc-emit` exits nonzero with a helpful error listing installed emitters.

### 10.4 Built-in Emitters

The `plcc` core package ships with three emitter plugins installed as dependencies:

- `plcc-emit-java` — generates a Java interpreter; `build()` runs `javac`.
- `plcc-emit-python` — generates a Python interpreter; no `build()`.
- `plcc-emit-plantuml` — generates a PlantUML class diagram; no `build()`.

A plain `pip install plcc` gets a user all three out of the box, supporting a standard PLCC course setup with zero additional installs.

Third-party emitters (`plcc-emit-rust`, `plcc-emit-typescript`, etc.) are published as independent PyPI packages. Installing one adds its target to `plcc-emit`'s discovery automatically.

## 11. First Non-Java Target: Python

The primary proof point for the retargeting architecture in v9 is `plcc-emit-python`. Python is chosen because:

- It is the highest-leverage adoption win. Many institutions teach Python as their primary language; their faculty cannot currently adopt PLCC.
- Its dynamic typing puts pressure on the code model abstraction. A code model that survives emission to Python without Java-ism leaks is much more likely to also survive emission to TypeScript, C#, or Rust later.
- Students in most CS curricula already know some Python, so the emitted interpreter is immediately readable to them.

`plcc-emit-python` must round-trip through the `languages` test repository (§13) in both its emitted code and its embedded runtime.

## 12. Distribution and Packaging

PLCC v9 is distributed through PyPI as `plcc`. All Level 0 primitives and Level 2 commands are console-script entry points declared in `pyproject.toml`. Installing the package provides every command on the user's `PATH`.

```
pip install plcc
```

Cross-platform by construction. No shell scripts, no environment variable setup, no OS-specific installers. The command a student or instructor runs to get a working PLCC is the same on Windows, macOS, and Linux.

Third-party emitters are separate PyPI packages following the naming convention `plcc-emit-<lang>`. They depend on `plcc` and register themselves under the `plcc.emitters` entry-point group.

```
pip install plcc plcc-emit-rust
```

This distribution model replaces the v8 model, which required cloning the repo and configuring environment variables — an adoption barrier that disproportionately affects students on Windows and instructors supporting multiple operating systems.

## 13. Repository Unification and Cutover

### 13.1 The current state

Two git repositories exist:

- `github.com/ourPLCC/plcc` — the canonical v8 repository. Current release: v8.0.2. 14 commits on `main` since the divergence point.
- `github.com/ourPLCC/plcc-ng` — the student-built Python rewrite. 282 commits on `main` since the divergence point.

Both repositories share a common ancestor: commit `fe08748` "build: prepare to unit test" (2024-05-01). They share the same root commit `b863951`. This means they can be unified with a normal `git merge`, without `--allow-unrelated-histories` or subtree tricks.

### 13.2 Unification procedure

All v9 development happens on a new `multi-lang` branch inside the `plcc` repository. The branch is created by merging plcc-ng's history into plcc:

```bash
cd plcc
git remote add ng https://github.com/ourPLCC/plcc-ng.git
git fetch ng
git checkout -b multi-lang
git merge ng/main
# resolve conflicts on README, devcontainer, license, etc.
```

Before the merge, plcc-ng's experimental version tags (`0.0.1` through `0.0.5`) are deleted from the local ref store so they do not enter the unified tag namespace. Only the commit history is preserved.

After the merge, `multi-lang` contains both lineages' files side by side. The refactor work happens on this branch: the new pipeline architecture grows, plcc-ng's existing spec-parsing and scan code is re-homed into Level 0 primitives, and legacy v8 code is progressively replaced.

### 13.3 Parallel release during transition

While `multi-lang` is under development, `main` remains the v8 release line. Faculty using existing learning materials see no disruption.

`multi-lang` publishes to PyPI as **prereleases** (`plcc==9.0.0a1`, `a2`, …, `rc1`). Early adopters who want to pilot the new architecture install with `pip install --pre plcc`. This surfaces real adoption feedback before cutover without committing anyone to the new version.

The `languages` test repository runs in CI against `multi-lang` throughout development, providing a continuous backwards-compatibility signal (§14).

### 13.4 Cutover

When `multi-lang` is ready and learning materials have been updated to match:

1. Tag `main` with `v8-final` so the pre-cutover state is recoverable forever.
2. Merge `multi-lang` → `main` through a normal `git merge` (or PR-based equivalent).
3. Publish `plcc==9.0.0` stable to PyPI from the merged `main`.
4. Archive the `plcc-ng` repository with a README pointing to the unified history in `plcc`.

The cutover is a single coordinated step, not a rename-and-archive choreography. All student contributions from both lineages remain visible in `git log` on the new `main`.

## 14. Backwards Compatibility

v9 provides **semantic backwards compatibility** for v8 grammar files, not bit-exact compatibility. A grammar file written against v8 passed to v9's `plcc-make` produces a working Java interpreter with the same runtime behavior. Generated class names, method signatures, and file layout may differ from v8's output; faculty tests of student programs continue to pass; faculty who inspected generated Java source may see differences.

### The `languages` test oracle

Backwards compatibility is not an aspiration in v9. It is a runnable, concrete signal. The `languages` repository contains the example languages referenced in PLCC's learning materials, along with tests that verify each language can be parsed by PLCC, have Java code generated, compiled, and run against example programs.

**v9 is considered backwards compatible when the full `languages` test suite passes against it.**

This test suite becomes part of v9's acceptance criteria. It runs in CI against `multi-lang` throughout development to catch regressions early rather than at the end. The Java emitter plugin (`plcc-emit-java`) is designed and tested against this suite.

The suite is not comprehensive — its coverage of runtime behavior is shallow — but it is concrete, already written, and exercises the full pipeline end to end against realistic grammars.

## 15. Revisions to Prior Brainstorming Decisions

This spec adjusts three decisions from earlier brainstorming sessions in light of the PyPI distribution commitment:

- **Decision #6** (originally: "Layer 2 commands compose Layer 0 primitives via shell scripts") is revised: Layer 2 commands are Python modules that orchestrate Layer 0 primitives using `subprocess.Popen`. Rationale: shell scripts do not work as pip entry points and break cross-platform installation on Windows.
- **Decision #11** (originally: `plcc-repl` as a Level 0 primitive that concatenates files and stdin with optional prompting) is revised: the input-assembly tool is eliminated. Layer 2 orchestrators open files with `pathlib` and read stdin with `sys.stdin`, writing bytes directly into the first subprocess's stdin pipe. Prompt logic consolidates in Layer 2 where tty detection already lives. Rationale: a Python-orchestrated pipeline does not need a dedicated input-assembly primitive; the job is trivial Python code.
- **Decision #12** (Layer 2 scripts detect tty and pass `--prompt` to both `plcc-repl` and the last pipeline stage) is simplified: Layer 2 orchestrators handle all prompting directly, since there is no longer a `plcc-repl` primitive to pass flags to.

These revisions preserve the spirit of the original decisions (single-responsibility primitives, honest Unix composition, responsive interactive mode) while removing machinery that existed only to work around limitations the new distribution model eliminates.

## 16. Deferred and Out of Scope

- **Pluggable verifiers.** Future extension; no work in v9.
- **Pluggable scanners and parsers.** The Level 0 primitives `plcc-tokens` and `plcc-tree` remain the only implementations in v9.
- **Level 1 intermediate compositions.** Deferred until a pedagogical use case emerges.
- **Non-OO target languages.** Retargeting in v9 is limited to modern OO languages.
- **Exact JSON schemas.** This spec establishes contracts and error-record discipline; schema details are the implementation plan's responsibility.
- **Migration of existing PLCC users to v9 on a timeline.** The cutover strategy supports parallel operation; the decision of when individual faculty migrate is their own.

## 17. Open Risks

- **Code model generality.** The code model is the retargeting pivot. If it accidentally encodes Java-isms, emission to Python will surface them, but late-discovered abstraction leaks could require rework of every emitter. Mitigation: emit to Python as early in the implementation plan as possible, before investing in the Java emitter's polish.
- **Runtime library drift across languages.** Each emitter plugin owns its runtime, so different languages' interpreters can drift in behavior. Mitigation: the `languages` test suite exercises Java runtime behavior; a parallel language-agnostic test suite should exercise Python runtime behavior as the Python emitter matures.
- **plcc-ng code that does not fit the pipeline shape.** plcc-ng's 282 commits include spec parsing and a scanner, but its internal structure shares dataclasses across package boundaries. Re-homing that code into Level 0 primitives with JSON contracts may reveal coupling that requires restructuring, not just relocation. Mitigation: the implementation plan begins with extracting `plcc-spec` as a standalone primitive to surface these issues early.
- **Learning materials lag.** The cutover gate is "learning materials have been updated." If this gate is held open indefinitely, the v8/v9 parallel window extends indefinitely. Mitigation: name a specific maintainer responsible for the learning materials update, with a review checkpoint after the Python emitter lands.
