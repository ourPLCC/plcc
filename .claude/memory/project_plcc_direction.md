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

6. **Layered tool structure** — Layer 0: single-responsibility primitives (JSON-in/JSON-out). Layer 2: user-facing commands (scan, parse, rep, plccmk) that compose primitives via shell scripts. Layer 1 (intermediate compositions) may or may not be needed; defer.

7. **Start with natural joints, split later** — begin with ~4 tools at the natural grammar-section boundaries (spec, scan, parse, gen). Split further only when there's a concrete reason (reuse, independent change, testing, pedagogical value).

8. **Intermediate files** — spec JSON and other intermediate artifacts are cached to avoid re-parsing, and are useful for debugging/teaching.

**Why:** Faculty adoption is gated on not requiring Java knowledge. The current PLCC generates only Java, limiting adoption to schools with Java in their curriculum.

**How to apply:** All architectural decisions should support the goal of adding new target languages with minimal effort. Each new target language should ideally require implementing only the interpreter generator tool.
