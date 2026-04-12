---
name: PLCC multi-language strategy
description: Key architectural decisions for making PLCC support multiple target languages beyond Java
type: project
---

Goal: Make PLCC adoptable by faculty whose students don't know Java. Primary audience for the decision is faculty (they decide adoption), but they think in terms of student experience.

Key decisions made during brainstorming (2026-04-11):

1. **Grammar format stays the same** — lexical/syntactic specs are language-agnostic, semantic `%%%` blocks are written in the target language.

2. **Mixed runtime is acceptable** — scanner and parser can be in a different language than the interpreter. Students need the target language installed; an additional dependency (e.g., Java or Python for scanner/parser) is acceptable if handled by containers/Codespaces.

3. **Scanner/parser should be readable** — not a black box. Code should be simple enough that a curious student can follow it even without expertise in the implementation language.

4. **Build on plcc-ng (Approach 1)** — refactor plcc-ng into Unix-pipeline architecture rather than starting from scratch. Preserves student work (449 commits, 148 Python files). Existing test suite provides safety during restructuring.

5. **Unix-pipeline architecture with JSON boundaries** — tools communicate via JSON (JSON Lines for tokens, JSON for AST/spec). JSON schemas define contracts between tools.

6. **Layered tool structure** — Layer 0: single-responsibility primitives (JSON-in/JSON-out). Layer 2: user-facing commands (scan, parse, rep, plccmk) that compose primitives via shell scripts. Layer 1 (intermediate compositions) deferred — may emerge for pedagogical use cases.

7. **Start with natural joints, split later** — begin with ~4-5 tools at the natural grammar-section boundaries. Split further only when there's a concrete reason (reuse, independent change, testing, pedagogical value).

8. **Intermediate files** — spec JSON and other intermediate artifacts are cached to avoid re-parsing, and are useful for debugging/teaching.

9. **Retargeting via code model (Approach B)** — two-phase generation:
   - `plcc-code-model`: spec JSON → code model JSON (language-neutral OO class hierarchy)
   - `plcc-emit-<language>`: code model JSON → source files in target language
   - Code model captures: classes, inheritance, attributes, constructors, method slots with opaque semantic blocks
   - Retargeting limited to modern OO languages — this is a pedagogical feature (class hierarchy, polymorphic dispatch is the programming model students learn)
   - PlantUML emitter (`plcc-emit-plantuml`) generates UML class diagrams from the same code model
   - Semantic block display is a presentation option on emitters (`--semantics=hide|note|comment|body`)

10. **Multiple semantic sections** — a grammar file can have multiple semantic sections, each targeting a different language. The divider syntax `% <tool> <language>` (already designed in plcc-ng) specifies the output directory name (tool) and target language for each section. This allows multiple interpreters for the same language from one grammar file. Generation loops over sections:
    ```
    plcc-code-model spec.json > code-model.json
    for each semantic section:
        plcc-emit-$language code-model.json --semantics=<section> --output=$tool/
    ```

11. **Pipeline architecture:**
    ```
    plcc-repl [files...] | plcc-scan spec.json | plcc-parse spec.json | interpreter
    ```
    - `plcc-repl`: concatenates file contents + stdin into text stream. No knowledge of program boundaries. Takes `--prompt` for initial prompt in interactive mode.
    - `plcc-scan`: tokenizes text stream, emits JSONL tokens. Stateless. Runs until EOF.
    - `plcc-parse`: consumes JSONL tokens, emits JSON ASTs. Knows program boundaries from grammar (start symbol). Long-running.
    - Interpreter: consumes JSON ASTs, evaluates, prints results. Maintains state across programs as language semantics require.
    - EOF propagates naturally through the pipe to shut down all stages.

12. **Interactive prompting:** Layer 2 scripts detect tty. If interactive, pass `--prompt="-->"` to `plcc-repl` (for initial prompt) and to the last pipeline stage (for subsequent prompts after each completed chunk). Prompts written to stderr. In batch mode, no `--prompt` flags are passed.

**Why:** Faculty adoption is gated on not requiring Java knowledge. The current PLCC generates only Java, limiting adoption to schools with Java in their curriculum.

**How to apply:** All architectural decisions should support the goal of adding new target languages with minimal effort. Each new target language requires only a new `plcc-emit-<language>` emitter.
