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

Last, we can try out our language's scanner, parser, and interpreter
against our samples.

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
$ rep -n < samples 
3
1
2
$
```

For more details, see [PLCC's Documentation](docs/README.md)
