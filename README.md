# PLCC - Programming Language Compiler Compiler

PLCC is designed for teaching and learning programming language concepts.

- [Licensed under GPL v3.0 or higher](LICENSE)
- [Chat with us on Discord](https://discord.gg/EVtNSxS9E2)
- [Report a problem or request a feature](https://github.com/ourPLCC/plcc/issues)
- [Read the paper](docs/PLCC-paper.pdf)
- [Learn how to contribute](docs/Contributing.md)

Related repositories:

- [ourPLCC/languages](https://github.com/ourPLCC/languages): Languages implemented in PLCC.
- [ourPLCC/course](https://github.com/ourPLCC/course): Course materials for
  teaching a Programming Languages course the uses PLCC.

## Options for Installation and Use

PLCC can be installed and used in different environments. The table below
may help you determine which option is best for you and your class.

| Option | Software Requirements | Non-Software Requirements | Consistent, Pre-configured Environment |
| ------ | ------------------- | ----------------------- | ---------- |
| GitPod |  Web Browser | Account on GitPod and hosting service (GitLab/GitHub/Bitbucket) <br> Knowledge of the above and Git | Yes |
| Docker | Docker Desktop | Minimal understanding of Docker | Yes |
| Native | Bash/Linux environment <br> Java >= 11 <br> Python >= 3.5 | System administration knowledge | No |

The advantages of GitPod or Docker are (1) few or no software dependencies
and (2) the ability to provide your class/developers a consistent development
environment with no installation necessary.

Having your students/developers perform native installations on their
individual machines can lead to unexpected challenges do to the variety of
different environments this creates. This can be mitigated by having your
IT staff install PLCC on a shared server or into a computer lab and having
your students/developers use those if their native install stops working
for them for some strange, inexplicable reason.

## Install PLCC for Use in GitPod

Add the following to `.gitpod.yml` in the root of
your GitLab/GitHub/Bitbucket repository.

```yaml
image: gitpod/workspace-full:latest
tasks:
  - name: Install PLCC
    command: |
        /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installers/plcc/install.bash)" >> ~/.bashrc
        exec bash
```

When the project is edited in a GitPod workspace, PLCC will be installed and
available in the environments terminal.

## Install for Use in Docker

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

Install `plcc-con` ...

* On macOS

  ```bash
  /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installers/plcc-con/install.bash)" >> ~/.zshrc
  ```

* On Windows >= 10, first
  [install WSL](https://learn.microsoft.com/en-us/windows/wsl/), and then in
  a Bash terminal in Ubuntu

  ```bash
  /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installers/plcc-con/install.bash)" >> ~/.bashrc
  ```

* On Linux

  ```bash
  /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installers/plcc-con/install.bash)" >> ~/.bashrc
  ```

After starting a new shell, you can start a shell inside a PLCC container
that has access to the files in your current directory.

```bash
plcc-con
```

Inside this shell, all of PLCC's commands are available. When you are done,
type `exit`.

You can also run a single PLCC command inside a PLCC container by passing
the command to `plcc-con`. For example, let's find out what version of
PLCC, Java, and Python are installed in the container.

```bash
plcc-con plcc --version
plcc-con java -version
plcc-con python3 --version
```

`plcc-con` is a Bash function that wraps the following Docker command

```bash
docker run --rm -it -v "${PWD}:/workdir" --user "$(id -u):$(id -g)" ghcr.io/ourplcc/plcc:latest
```

## Native Install

### Install a Bash/Linux environment

* On Windows >= 10,
please [install WSL](https://learn.microsoft.com/en-us/windows/wsl/). Then run
a Terminal and open Ubuntu from its dropdown menu. You are now running in
Bash inside an Ubuntu virtual machine. Use this environment to install
and use PLCC. From now on, when an instruction refers to Linux, make sure
you are running in this environment. Including the next line.

* On Linux, we assume you are running in Bash on a Debian-based Linux
distributed (this includes Ubuntu) which uses `apt-get` as its package
manager. If this is not your situation, you will have to adapt the instructions
appropriately for your environment. 

* On macOS, please [install Homebrew](https://brew.sh/).

### Install PLCC

* On macOS (remove "`>> ~/.zshrc`" if you would like to update this file manually)

  ```bash
  brew install curl git
  /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installers/plcc/install.bash)" >> ~/.zshrc
  ```

* On Linux or Windows under [WSL](https://learn.microsoft.com/en-us/windows/wsl/) (remove "`>> ~/.bashrc`" if you would like to update this file manually)

  ```bash
  sudo apt-get update
  sudo apt-get install curl git
  /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installers/plcc/install.bash)" >> ~/.bashrc
  ```

### Install Java

Check if you have `java` and `javac` >= 11

```
java -version
javac -version
```

If you are missing either, or if their versions don't match, or either is
outdated, please [install SDKMAN!](https://sdkman.io/install),
and use it to install Java.

### Install Python

Check if you have Python >= 3.5

```bash
python3 --version
```

If not, then install Python.

* On macOS

  ```bash
  brew install python3
  ```

* On Linux or Windows under [WSL](https://learn.microsoft.com/en-us/windows/wsl/)

  ```bash
  sudo apt-get update
  sudo apt-get install python3
  ```

## Use

Now that you have a Linux-like, Bash-like environment installed with
PLCC and its dependencies, here's how you use it.

```bash
$EDITOR samples        # Write sample programs in your language.
$EDITOR grammar        # Write a grammar file defining your language.
plccmk -c grammar      # Compile grammar into a scanner, parser, and interpreter.
scan < samples         # Run the scanner on your samples.
parse -n -t < samples  # Run the parser on your samples.
rep -n -t < samples    # Run the interpreter on your samples.
```

### Example

Let's create a scanner, parser, and interpreter to evaluate subtraction
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

## Commands

```
plcc file

  Run plcc.py on 'file' to generate code in a directory named 'Java/'.


plccmk [-c] [--json_ast] [file]

  Run plcc.py on 'file' and compile its results.

  '-c' Removes 'Java/' before regenerating it.
  '--json_ast' add support to print JSON ASTs.
      Required if you want to call parse with --json_ast.
  'file' defaults to 'grammar'


scan [file...]

    Run Java/Scan on each file and then stdin printing recognized tokens.


parse [-t] [-n] [--json_ast] [file...]

  Run Java/Parser on each file and then stdin,
  printing OK for recognized programs and errors otherwise.

  '-t' Print trace (i.e., parse tree).
  '-n' Suppress prompt.
  '--json_ast' print JSON AST to stdout.


rep [-t] [-n] [file...]

    Run Java/Rep on each file and then stdin.
    REP Reads, Executes, and Prints each program in the input.

    '-t' Print trace (i.e., parse tree).
    '-n' Suppress prompt.
```

To print a JSON AST for a program, pass `--json_ast` to both `plccmk`
and `parse`, like so:

```bash
plccmk --json_ast -c YOUR_GRAMMAR_FILE
parse --json_ast < YOUR_PROGRAM_FILE
```

## Grammar Files

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
  * [java.util.regex.Pattern](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/regex/Pattern.html):
    Complete reference of regex syntax that PLCC accepts.
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

#### Parse Algorithm

**TL;DR - Start each alternative definition for the same non-terminal with a different token.**

The parsing algorithm is a recursive-descent parser that parses languages
in LL(1). Let's take a look.

Each rule in the syntactic spec turns into a static parse method embedded
in the class generated by the same rule. For example,

```
<prog> ::= <exp>
<exp>WholeExp ::= <WHOLE>
<exp>SubExp ::= MINUS LP <exp>exp1 COMMA <exp>exp2 RP
```

This generates (slightly simplified):

```java
class Prog{
  static Prog parse(Scan scn$) {
    Exp exp = Exp.parse(scn$);
    return new Prog(exp);
  }
}
class Exp{
  public static Exp parse(Scan scn$) {
    Token t$ = scn$.cur();
    Token.Match match$ = t$.match;
    switch(match$) {
    case WHOLE:
      return WholeExp.parse(scn$);
    case MINUS:
      return SubExp.parse(scn$);
    default:
      throw new PLCCException("Parse error");
    }
  }
}
class WholeExp{
  static WholeExp parse(Scan scn$) {
    Token whole = scn$.match(Token.Match.WHOLE);
    return new WholeExp(whole);
  }
}
class SubExp{
  static SubExp parse(Scan scn$) {
    scn$.match(Token.Match.MINUS);
    scn$.match(Token.Match.LP);
    Exp exp1 = Exp.parse(scn$);
    scn$.match(Token.Match.COMMA);
    Exp exp2 = Exp.parse(scn$);
    scn$.match(Token.Match.RP);
    return new SubExp(exp1, exp2);
  }  
}
```

Parsing starts with the start symbol: here `Prog`.
Each parse method is responsible for matching the structure of the RHS of
the syntactic rule it represents. It does so from left to right.
Tokens are matched directly by telling the scanner what type of token
it should match and consume. Non-terminals are matched by calling their
parse method which matches its structure, returning an instance of that
non-terminal's class.

The parse function of an abstract base class (e.g., in `Exp` above)
determines which subclass's method to call by looking at the next token.
For this reason, it's important that when defining a language's syntax
that **each alternative definition for the same non-terminal start with
a different token**.

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
  class representing a non-terminal that has alternatives: see `Exp` above.
  Then override this method in the subclasses representing the
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

## Copyright and Licensing

ourPLCC is a community of developers that maintain a number of projects
related to PLCC. The contents of the projects were originally created
by Timothy Fossum <plcc@pithon.net>.

Thank you Tim!

* Copyright (C) 2023  Timothy Fossum <plcc@pithon.net>
* Copyright (C) 2023- PLCC Community <https://discord.gg/EVtNSxS9E2>
* License: [GPL v3.0 or higher](LICENSES/GPL-3.0-or-later.txt).

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the
[GNU General Public License](LICENSES/GPL-3.0-or-later.txt)
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Third Party Libraries

PLCC uses and distributes [Jackson JSON Processor](https://github.com/FasterXML),
under the [Apache 2.0](LICENSES/Apache-2.0.txt).
