# Commands

## `plccmk`

`plccmk` reads a grammar file; generates code to scan, parse,
and evalute programs written in the language defined in the
grammar; and compiles the generated code. By default it generates
and compiles Java code. It places the generated and compiled code
in a subdirectory named `Java`. When called with the `-c` option,
it first deletes `Java` before regenerating and compiling code.
This is a good practice.

```bash
$ ls
grammar
$ plccmk -c grammar
Nonterminals (* indicates start symbol):
  <exp>
 *<program>

Abstract classes:
  Exp

Java source files created:
  Exp.java
  Program.java
  SubExp.java
  WholeExp.java
$ ls
Java    grammar
```

After running `plccmk`, assuming there are no errors, you are ready
to run your language's scannar, parser, or evaluator using PLCC's
`scan`, `parse`, or `rep` commands respectively. These commands
are each explained in the following sections.

## `scan`

`scan` runs the compiled scanner in the `Java/` directory
(`Java/Scan.class`). The scanner reads a program written in
the language defined by the grammar and prints the tokens
it recognizes.
