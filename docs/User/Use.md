# Using PLCC

This document will help you learn how to use PLCC.

## 1. An extremely brief example

```bash
# Write a test program in the language we are inventing.
vim prog.lang

# Write a grammar file defining the language's syntax and semantics.
vim lang.plcc

# Generate a scanner, parser, and a rep-loop for your language.
plccmk -c lang.plcc

# Test your scanner to see if it produces reasonable tokens.
scan < prog.lang

# Test your parser to see if it produces a reasonable parse tree.
parse -n -t < prog.lang

# Test your semantics by running the rep loop to see if it behaves reasonably.
rep -n < prog.lang
```

## 2. A more expansive example

In this section we will compile and run the scanner, parser, and rep-loop
for the GINGER language. This language can be found in the `GINGER/`
subdirectory of the
[ourPLCC/languages](https://github.com/ourPLCC/languages) repository.
If you would like to follow along with this example, download this
repository into your PLCC installed environment, and then reposition your
shell into its `GINGER/` directory. For example, in a Bash environment
with Git installed,

```bash
git clone https://github.com/ourPLCC/languages
cd languages/GINGER
```

`GINGER/` contains the following files.

* ginger.jpeg - The Farside comic that inspired this language.
* grammar - The definition of the GINGER language.
* what-we-say - A sample "program" written in the GINGER language.

The comic in ginger.jpeg (shown below) depicts what the GINGER language
does. Programs written in GINGER are English documents. When evaluated
by GINGER, it reproduces the program but with all words and punctuation
other than the word Ginger is converted to "blah", and all occurrences of
"Ginger" converted to all caps "GINGER".

![Gary Larson's Farside comic depicting what Dog's hear](images/ginger.jpeg)

`grammar` defines the syntax and semantics of GINGER. This is written using
the the PLCC language for defining languages. We'll cover its syntax later.

Last, `what-we-say` is a "program" written in the GINGER language. Its
contents are as follows.

```
Okay, Ginger! I've had it! You stay out of the garbage!
Do you understand, Ginger? Stay out of the garbage, or else!
```

First, we use `plccmk` to build the scanner, parser, and rep-loop for
the GINGER language.

```bash
$ plccmk -c grammar
Nonterminals (* indicates start symbol):
 *<whatwesay>
  <word>
  <words>

Abstract classes:
  Word

Java source files created:
  Blah.java
  Ginger.java
  Punct.java
  Whatwesay.java
  Word.java
  Words.java
```

`plccmk` generates and compiles Java code for scanning,
parsing, and interpreting programs written in the GINGER language.
It places the results are placed in `Java/`.

Now we can use PLCC's `scan`, `parse`, and `rep` commands to run the
generated programs on programs written in GINGER.
For example, we can run GINGER's scanner using PLCC's `scan` command.

```bash
$ scan < what-we-say
   1: BLAH 'Okay'
   1: PUNCT ','
   1: PUNCT ' '
   1: GINGER 'Ginger'
   1: PUNCT '!'
   1: PUNCT ' '
   1: BLAH 'I've'
   1: PUNCT ' '
   1: BLAH 'had'
   1: PUNCT ' '
   1: BLAH 'it'
   1: PUNCT '!'
   1: PUNCT ' '
   1: BLAH 'You'
   1: PUNCT ' '
   1: BLAH 'stay'
   1: PUNCT ' '
   1: BLAH 'out'
   1: PUNCT ' '
   1: BLAH 'of'
   1: PUNCT ' '
   1: BLAH 'the'
   1: PUNCT ' '
   1: BLAH 'garbage'
   1: PUNCT '!'
   1: NL '
'
   2: BLAH 'Do'
   2: PUNCT ' '
   2: BLAH 'you'
   2: PUNCT ' '
   2: BLAH 'understand'
   2: PUNCT ','
   2: PUNCT ' '
   2: GINGER 'Ginger'
   2: PUNCT '?'
   2: PUNCT ' '
   2: BLAH 'Stay'
   2: PUNCT ' '
   2: BLAH 'out'
   2: PUNCT ' '
   2: BLAH 'of'
   2: PUNCT ' '
   2: BLAH 'the'
   2: PUNCT ' '
   2: BLAH 'garbage'
   2: PUNCT ','
   2: PUNCT ' '
   2: BLAH 'or'
   2: PUNCT ' '
   2: BLAH 'else'
   2: PUNCT '!'
   2: NL '
'
```

The scanner prints each token it finds along with the line number on which
it found it.

We can run GINGER's parser on the same example program.

```bash
$ parse -t -n < what-we-say
   1: <whatwesay>
   1: | <words>
   1: | | <word>:Blah
   1: | | | BLAH "Okay"
   1: | | <word>:Punct
   1: | | | PUNCT ","
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Ginger
   1: | | | GINGER "Ginger"
   1: | | <word>:Punct
   1: | | | PUNCT "!"
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Blah
   1: | | | BLAH "I've"
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Blah
   1: | | | BLAH "had"
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Blah
   1: | | | BLAH "it"
   1: | | <word>:Punct
   1: | | | PUNCT "!"
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Blah
   1: | | | BLAH "You"
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Blah
   1: | | | BLAH "stay"
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Blah
   1: | | | BLAH "out"
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Blah
   1: | | | BLAH "of"
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Blah
   1: | | | BLAH "the"
   1: | | <word>:Punct
   1: | | | PUNCT " "
   1: | | <word>:Blah
   1: | | | BLAH "garbage"
   1: | | <word>:Punct
   1: | | | PUNCT "!"
   1: | NL "
"
OK
   2: <whatwesay>
   2: | <words>
   2: | | <word>:Blah
   2: | | | BLAH "Do"
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Blah
   2: | | | BLAH "you"
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Blah
   2: | | | BLAH "understand"
   2: | | <word>:Punct
   2: | | | PUNCT ","
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Ginger
   2: | | | GINGER "Ginger"
   2: | | <word>:Punct
   2: | | | PUNCT "?"
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Blah
   2: | | | BLAH "Stay"
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Blah
   2: | | | BLAH "out"
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Blah
   2: | | | BLAH "of"
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Blah
   2: | | | BLAH "the"
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Blah
   2: | | | BLAH "garbage"
   2: | | <word>:Punct
   2: | | | PUNCT ","
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Blah
   2: | | | BLAH "or"
   2: | | <word>:Punct
   2: | | | PUNCT " "
   2: | | <word>:Blah
   2: | | | BLAH "else"
   2: | | <word>:Punct
   2: | | | PUNCT "!"
   2: | NL "
"
OK
```

The `OK`s in the output indicate that the parser successfully parsed an
instance of a GINGER program. We see that there are two such `OK`s. That
means there are two GINGER programs in this one file. We also see that
the output contains two trees. These are traces of the parse algorithm
and are effectively the parser tree of the two programs. They were printed
because we passed `-t` to `parse`. The parser is designed to be ran
interactively. Since we are redirecting input from a file, we passed
`-n` to `parse` to suppress the prompt it generates by default.

Last, there is PLCC's `rep` command which we use to run GINGER's rep-loop
(read-evaluate-print loop), which interprets programs written in GINGER.

```bash
$ rep -n < what-we-say
blah, Ginger! blah blah blah! blah blah blah blah blah blah!
blah blah blah, Ginger? blah blah blah blah blah, blah blah!
```

Like `parse`, `rep` is designed to run interactively. The `-n` passed
to it suppresses its prompt. We could also pass `-t` and have it display
both the parse trace and the results of interpreting each program in
GINGER.

## 3. What's next

Now that you have a rough idea of how to use PLCC, you are ready to
learn the structure of a [PLCC grammar file](Grammar.md).