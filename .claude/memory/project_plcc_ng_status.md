---
name: plcc-ng project status
description: What plcc-ng has built and what's missing as of 2026-04-11
type: project
---

plcc-ng (https://github.com/ourPLCC/plcc-ng) is a clean-room rewrite of PLCC built by students using TDD.

**Completed:** spec parsing (lexical, syntactic, semantic sections), working scanner, LL(1) validation, spec CLI (outputs JSON), scan CLI (outputs tokens).

**Not built:** parser runtime, code generator/interpreter generator.

**Architecture:** well-structured Python monolith with clean internal modules but shared dataclasses across boundaries (Line, LexicalRule, Token imported across packages). 148 Python source files across packages: lines, scan, spec (with lexical, syntax, semantics, rough sub-packages).

**Why:** This is the codebase being refactored into the Unix-pipeline architecture per the multi-language strategy decisions.

**How to apply:** When starting implementation, begin by extracting the spec parser as the first standalone tool, since downstream tools depend on its JSON output format.
