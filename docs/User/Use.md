# Using PLCC

This document will help you learn how to use PLCC's commands.
For a more complete reference of commands see [Command Reference](Commands.md).
For a description of PLCC's grammar files see [Grammar Files](Grammars.md).

## 1. Overview

A common workflow in PLCC is to

1. Define you language's syntax and semantics in a grammar file.
2. Compile your grammar file into a scanner, parser, and interpreter.
3. Test your scanner, parser, and/or interpreter on sample programs.

In a Bash environment, this would look something like this
(the output of each command is not shown).

```bash
$ $EDITOR grammar        # 1. Define syntax and semantics.
$ plccmk -c grammar      # 2. Compile into a scanner, parser, and interpreter.
$ scan < samples         # 3a. Test the scanner with sample programs.
$ parse -n -t < samples  # 3b. Test the parser with sample programs.
$ rep -n -t < samples    # 3c. Test the interpreter with sample programs.
```

Of course no one actually implements a lanugage with linearly.
More realistically, we usually start with the scanner; writing
a small lexical specification, compiling, and testing the scanner;
repeating as necessary. Once our scanner is working, we move on
to the parser; defining the syntactic structure of our language,
recompiling, and testing our parser; repeating as necessary,
possibly updating our lexical specification and retesting the
scanner too. With our scanner and parser working, we last move
on to semantics; incrementally defining, compiling, and testing
our interpreter; making adjustments to and retesting the lexical
and syntactic specification as necessary.

Let's take a closer look at each of the commands in our example above.

## 2. `plccmk`

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

## 3. `scan`

`scan` runs the compiled scanner in the `Java/` directory
(`Java/Scan.class`). The scanner reads a program written in
the language defined by the grammar and prints the tokens
it recognizes.
