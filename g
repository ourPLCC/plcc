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

