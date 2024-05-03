from .stubs import Stubs


class JavaStubs(Stubs):
    def __init__(self, stubs=None):
        super().__init__(stubs)

    def getLineComment(self):
        return '//'

    def getBlockCommentStart(self):
        return "/*"

    def getBlockCommentEnd(self):
        return "*/"

    def makeFieldDeclaration(self, type, name):
        return f'public {type} {name};'

    def makeFieldInitializer(self, name):
        return f'this.{name} = {name};'

    def makeParameterDeclaration(self, type, name):
        return f'{type} {name}'

    def makeExtendsClause(self, type):
        return f' extends {type}'

    def makeCase(self, value):
        return f'case {value}:'

    def makeParseCaseReturn(self, cls):
        return f'return {cls}.parse(scn$,trace$);'

    def makeStub(self, cls, lhs, ext, ruleString, decls, params, inits, parse):
        return f"""\
//{cls}:top//
//{cls}:import//
import java.util.*;

// {ruleString}
public class {cls}{ext} /*{cls}:class*/ {{

    public static final String $className = "{cls}";
    public static final String $ruleString =
        "{ruleString}";

{decls}

    public {cls}({params}) {{
//{cls}:init//
{inits}
    }}

    public static {cls} parse(Scan scn$, Trace trace$) {{
        if (trace$ != null)
            trace$ = trace$.nonterm("{lhs}", scn$.lno);
{parse}
    }}

//{cls}//
}}
"""

    def makeAbstractStub(self, base, ext, cases):
        return f"""\
//{base}:top//
//{base}:import//
import java.util.*;

public abstract class {base}{ext} /*{base}:class*/ {{

    public static final String $className = "{base}";
    public static {base} parse(Scan scn$, Trace trace$) {{
        Token t$ = scn$.cur();
        Token.Match match$ = t$.match;
        switch(match$) {{
{cases}
        default:
            throw new PLCCException(
                "Parse error",
                "{base} cannot begin with " + t$.errString()
            );
        }}
    }}

//{base}//
}}
"""

