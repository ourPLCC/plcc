# PLCC

PLCC is a Programming Language Compiler Compiler designed for use in
a Programming Languages course.

- License: [GPLv3.0 or higher](LICENSE)
- Need help? [Chat with us on Discord](https://discord.gg/EVtNSxS9E2).
- Report a problem or request a feature? [Open an issue](https://github.com/ourPLCC/plcc/issues).
- [PLCC's Documentation](docs/README.md)

## Quick Start

### Install

If the following don't work for you or your context,
please see [PLCC's Documentation](docs/README.md) for more options.

**Bash (Linux, macOS, Windows via WSL)**

Requires bash, curl, and git.

```bash
/bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)"
```

**Docker (any OS)**

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

Start a shell (Linux like shell including PowerShell) in the PLCC container.

```bash
docker run --rm -it -v "$PWD:/workdir" ghcr.io/ourplcc/plcc:latest
```

**GitPod (any OS)**

Add the following to `.gitpod.yml` in the root of your GitLab/GitHub/Bitbucket
repository:

```yaml
image: gitpod/workspace-full:latest

tasks:
  - name: Install PLCC
    command: |
        /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)" >> ~/.bashrc
        exec bash
```

### Use

```bash
$ $EDITOR samples        # Write sample programs in your language.
$ $EDITOR grammar        # Write a grammar file defining your language.
$ plccmk -c grammar      # Compile grammar into a scanner, parser, and interpreter.
$ scan < samples         # Run the scanner on your samples.
$ parse -n -t < samples  # Run the parser on your samples.
$ rep -n -t < samples    # Run the interpreter on your samples.
```

For example. We want to create scanner, parser, and interpreter for a
language that allows us to express subtraction of whole numbers in
prefix notation: e.g., -( -(4,1), -(3,2) ). The interpreter will evaluate
such expressions and print the result.

We create a file named `samples` whose contents contains three example
programs in our new language.

```
3

-(3,2)

-(-(4,1), -(3,2))
```

Next, let's define our language in a file named `grammar`:

```java
skip WHITESPACE '\s+'
token WHOLE '\d+'
token MINUS '\-'
token LP '\('
token RP '\)'
token COMMA ','
%
<prog> ::= <exp>
<exp>WholeExp ::= <WHOLE>
<exp>SubExp ::= MINUS LP <exp>exp1 COMMA <exp>exp2 RP
%
Prog
%%%
  public void $run() {
    System.out.println(exp.eval());
  }
%%%

Exp
%%%
  abstract public int eval();
%%%

SubExp
%%%
  public int eval() {
    return exp1.eval() - exp2.eval();
  }
%%%

WholeExp
%%%
  public int eval() {
    return Integer.parseInt(whole.toString());
  }
%%%
```

Now, we compile our grammar.

```bash
$ plccmk -c grammar
Nonterminals (* indicates start symbol):
  <exp>
 *<prog>

Abstract classes:
  Exp

Java source files created:
  Exp.java
  Prog.java
  SubExp.java
  WholeExp.java
```

Now, we can try our language's scanner.

```bash
gitpod /workspace/plcc (StoneyJackson-docs) $ scan < samples 
   1: WHOLE '3'
   3: MINUS '-'
   3: LP '('
   3: WHOLE '3'
   3: COMMA ','
   3: WHOLE '2'
   3: RP ')'
   5: MINUS '-'
   5: LP '('
   5: MINUS '-'
   5: LP '('
   5: WHOLE '4'
   5: COMMA ','
   5: WHOLE '1'
   5: RP ')'
   5: COMMA ','
   5: MINUS '-'
   5: LP '('
   5: WHOLE '3'
   5: COMMA ','
   5: WHOLE '2'
   5: RP ')'
   5: RP ')'
```

Now try the parser.

```bash
$ parse -t -n < samples 
   1: <prog>
   1: | <exp>WholeExp
   1: | | WHOLE "3"
OK
   3: <prog>
   3: | <exp>SubExp
   3: | | MINUS "-"
   3: | | LP "("
   3: | | <exp>WholeExp
   3: | | | WHOLE "3"
   3: | | COMMA ","
   3: | | <exp>WholeExp
   3: | | | WHOLE "2"
   3: | | RP ")"
OK
   5: <prog>
   5: | <exp>SubExp
   5: | | MINUS "-"
   5: | | LP "("
   5: | | <exp>SubExp
   5: | | | MINUS "-"
   5: | | | LP "("
   5: | | | <exp>WholeExp
   5: | | | | WHOLE "4"
   5: | | | COMMA ","
   5: | | | <exp>WholeExp
   5: | | | | WHOLE "1"
   5: | | | RP ")"
   5: | | COMMA ","
   5: | | <exp>SubExp
   5: | | | MINUS "-"
   5: | | | LP "("
   5: | | | <exp>WholeExp
   5: | | | | WHOLE "3"
   5: | | | COMMA ","
   5: | | | <exp>WholeExp
   5: | | | | WHOLE "2"
   5: | | | RP ")"
   5: | | RP ")"
OK
```

And finally the interpreter.

```bash
$ rep -n < samples 
3
1
2
$
```

### Commands

```
plcc file
                        runs plcc.py on 'file', which generates
                            code in a directory named 'Java/'.
plccmk [-c] [file]
                        runs plcc.py on file and compiles its results.
                        '-c' Remove 'Java/' before regenerating it.
                        'file' defaults to 'grammar'
scan [file...]
                        Run Java/Scan on each file and then stdin.
                            Scans input printing recognized token.
parse [-t] [-n] [file...]
                        Run Java/Parser on each file and then stdin.
                            Scans and parses input, printing OK for recognized
                            programs and error otherwise.
                        '-t' Print trace (i.e., parse tree).
                        '-n' Suppress prompt.
rep [-t] [-n] [file...]
                        Run Java/Rep on each file and then stdin.
                            REP = Read, Execute, and Print loop.
                            Scans, parses, and evaluates each program
                            in the input.
                        '-t' Print trace (i.e., parse tree).
                        '-n' Suppress prompt.
```

## Grammar

A grammar file consist of three sections, separated by a percent on a line
by itself.

```
[Lexical specification]
%
[Syntactic specification]
%
[Semantic specification]
```

PLCC generates a different tool from each section.

```
Lexical specification   => Scanner
Syntactic specification => Parser
Semantic specification  => Interpreter
```

The tools are dependent on each other as follows:

```
Interpreter depends-on Parser depends-on Scanner
```

Likewise the corresponding sections are dependent on
each other:

```
Semantic depends-on Syntactic depends-on Lexical
```

For example, this means, if you only need to build a parser,
you may omit the semantic specification, but not the
lexical and syntactic specifications.

### Lexical Specification

The lexical specification is used to build a scanner.
A scanner scans an input string from left to right looking
for patterns. When it finds a pattern it recognizes, it
either emits it as a named token, or skips it. If it does
not recognize any patterns, it emits an error.

In the lexical specification, we define named patterns that
will be either emitted as tokens or skipped.

Each rule starts with `token` or `skip`, this is followed by
its name in all caps and underscores, and ends with a regular
expression enclosed in either single or double quotes.

In this section, lines starting with `#` are comments.

Here's an annotated example of a lexical specification

```
# Match and consume one or more whitespace characters,
# but do not emit a token.
skip WHITESPACE '\s+'

# Match and consume one or more digit characters,
# and emit them as a WHOLE token.
token WHOLE '\d+'

# And so on...
token MINUS '\-'
token LP '\('
token RP '\)'
token COMMA ','
```

#### Regular Expressions

Patterns are defined using Java's regular expression syntax.
Here are some good resources for regex:

* [java.util.regex.Pattern](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/regex/Pattern.html): Complete reference of syntax.
* [RegexOne](https://regexone.com/): Great set of interact lessons.
* [regex101](https://regex101.com/): Great tool for building, testing, and visualizing.

#### The Scanning Algorithm

The scanner is implemented in Java, but here is
a partial pseudo-Python implementation to illustrate it.

```python
def scan(rules, unmatched):
  while len(unmatched) > 0:
    rule = get_rule_to_apply(rules, unmatched)
    if rule is None:
      raise Exception('Error: no rule matched')
    n = rule.get_match_length(unmatched)
    matched = unmatched[:n]
    unmatched = unmatched[n:]
    if rule.is_token():
      yield Token(rule.name, matched)

def get_rule_to_apply(rules, unmatched)
  rules = get_rules_that_match_start(rules, unmatched)
  rules = get_rules_with_longest_match(rules, unmatched)
  return get_rule_appearing_first_in_spec(rules)
```

Each pass of the loop selects a rule to apply to the
start of the unmatched input string. The rule selected
is the rule that matches the most characters
(the ***longest***), and the one that appears ***first***
in the spec if there is a tie for ***longest***. 
We call this this ***first-longest-match*** rule.
The substring matched by the selected rule are removed
from the front of the unmatched string. If the selected
rule is a token rule, then the matched string is emitted
as a Token along with the name of the rule. This continues
until the unmatched string is empty, or no rules match
the start of the unmatched string (which is an error).

### Syntactic specification

### Semantic specification
