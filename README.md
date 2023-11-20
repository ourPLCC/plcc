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

An external file can be include from anywhere in the spec.

```
include external_file_name
```

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

A syntax specification is a flavor of
[BNF (Backus-Naur From)](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form).

```
<prog> ::= <exp>
<exp>WholeExp ::= <WHOLE>
<exp>SubExp ::= MINUS LP <exp>exp1 COMMA <exp>exp2 RP
```

* Non-terminal are always enclosed in angles and start
  with a lowercase. E.g., `<exp>`.
* Terminals are always all-caps, and MAY be enclosed
  in angles. E.g., `<WHOLE>` and `MINUS`
* Any symbol enclosed in angles will be included in
  the parse tree. So `<WHOLE>` will be included,
  but `MINUS` will not.
* When a symbol appears more than once on the right-hand
side of a rule, each must be given a name to distinguish it from the others. E.g., `<exp>exp1`, the distinguishing name is `exp1`. That name must start with a lower case.
* When a non-terminal appears multiple times on the left-hand-side, each must be given a name to distinguish it
from the others. The name must start with an upper case letter. E.g., `<exp>SubExp`, the distinguishing name is `SubExp`.
* Alternatives definitions for a non-terminal is accomplished by
providing multiple rules that define the same non-terminal.

#### Parse Tree Class Hierarchy

PLCC translates semantic rules into a class hierarchy. For example:

```
<prog> ::= <exp>
<exp>WholeExp ::= <WHOLE>
<exp>SubExp ::= MINUS LP <exp>exp1 COMMA <exp>exp2 RP
```

becomes (many details have been omitted):

```Java
class Prog extends _Start { Exp exp; }
abstract class Exp {}
class WholeExp extends Exp { Token whole; }
class SubExp extends Exp { Exp exp1; Exp exp2; }
```

* A class is generated for the non-terminal defined by a rule (the LHS) with instance variables defined for each captured symbols (e.g., `<>`) on the RHS.
* The first rule defines the start symbol,
and its class inherits from _Start.
* A non-terminal defined more than once becomes an abstract base class,
and the distinguishing names become its subclasses.
* Tokens always have the type of Token.

#### Repetition Rule

The repetition rule simplifies defining a repeating structure.

```
<pairs> **= LP <WHOLE>x <WHOLE>y RP +COMMA
```

`<pairs>` matches zero or more (x,y) pairs separated by comma: e.g., `(3 4), (5 6), (7 8)`. The separator clause (e.g., `+COMMA`) is optional. E.g.,

PLCC translates the above rule into:

```java
class Pairs { List<Val> xList; List<Val> yList; }
```

The captured symbols become parallel lists. That is `xList.get(0)`
corresponds to `yList.get(0)`.

### Semantic specification

The semantic specification injects code into
the classes generated from the syntactic specification.

```java
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

* The class representing the start symbol should override the `$run`
  method. Execution of the interpreter begins here: see `Prog` above.
* To enable polymorphism, add an abstract method to the abstract base
class representing a non-terminal that has alternatives: see `Exp` above. Then override this method in the subclasses representing the
concrete alternatives: see `SubExp` and `WholeExp` above.


#### Hooks

By default, you can only inject code at the end of a class.
Hooks allow you to inject code elsewhere.

* `<classname>:top` - Top of file.
* `<classname>:import` - Add `import`s.
* `<classname>:class` - Declare `extends` or `implements`.
* `<classname>:init` - Constructor.

As an example, we update our original example by replacing the
definition fr WholeExp with this.

```java
WholeExp:import
%%%
import java.util.HashMap;
%%%

WholeExp
%%%
  public static HashMap<Integer,Integer> =
    new HashMap<Integer,Integer>();

  public int eval() {
    int x = Integer.parseInt(whole.toString());
    checkDuplicate(x);
    return x;
  }

  public void checkDuplicate(int x) {
    if (seen.containsKey(x)) {
      System.out.println("Duplicate: " + x);
    } else {
      seen.put(x, x);
    }
  }
%%%
```

Now our interpreter reports when it sees a duplicate whole number.

#### Adding additional Java files/classes

Entire Java files can be added by naming a class that is not
generated from the syntactic specification.

```java
Helper
%%%
import java.util.List;

public class Helper {
  \\ ...
}
%%%
```
