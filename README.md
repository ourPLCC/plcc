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


#### Example

Create a scanner, parser, and interpreter to evaluate subtraction
expressions. Here are some example input programs (file `samples`).

```
3

-(3,2)

-(-(4,1), -(3,2))
```

Write a `grammar` file.

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

Compile it.

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

Test the scanner.

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

Test the parser.

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

Test the interpreter.

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

A grammar file consist of three sections separated by a line containing
a single percent.

```
[Lexical specification]
%
[Syntactic specification]
%
[Semantic specification]
```

PLCC generates a different tool from each section.

```
Lexical   GENERATES Scanner
Syntactic GENERATES Parser
Semantic  GENERATES Interpreter
```

The tools are dependent on each other as follows:

```
Interpreter DEPENDS-ON Parser DEPENDS-ON Scanner
```

Likewise the corresponding sections are dependent on
each other:

```
Semantic DEPENDS-ON Syntactic DEPENDS-ON Lexical
```

For example, to build a parser, you don't need a semantic spec,
but you do need a lexical and syntactic specs.

### Lexical Specification

The lexical specification contains `token` and `skip` rules,
one per line. Lines starting with `#` are comments.
For example,

```
# Skip rules discard the text the match.
skip WHITESPACE '\s+'

# Token rules emits a Token containing their name and the match.
token PLUS "\+"
token WORD "\w+"
```

* Names must be all-caps and may have underscores.
* Patterns are regular expressions (regex) enclosed in either single
or double quotes. Here are some resources on regex.
  * [java.util.regex.Pattern](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/regex/Pattern.html): Complete reference of regex syntax that PLCC accepts.
  * [RegexOne](https://regexone.com/): Great set of interact lessons.
  * [regex101](https://regex101.com/): Great tool for building, testing, and visualizing.

#### Scan algorithm

Partial, pseudo-Python implementation of PLCC's scan algorithm.

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

Each iteration selects and applies a rule to the
start of the unmatched input string. The rule that
appears first in the spec with the longest match is
selected (the ***First-Longest-Match-Rule***).
If no such rule exists, then an error is emitted.

### Syntactic specification

### Semantic specification
