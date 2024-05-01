from .base import CodeGenerator


class JavaCodeGenerator(CodeGenerator):
    def __init__(self, stubs):
        super().__init__(spec, stubs)


spec = {
    "abstractStubFormatString" : """\
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
""",

    "stubFormatString" : """\
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
""",
    "extendFormatString" : ' extends {cls}',
    "declFormatString" : 'public {fieldType} {field};',
    "initFormatString" : 'this.{field} = {field};',
    "paramFormatString" : '{fieldType} {field}',
    "semFlag" : 'semantics',
    "lineComment" : '//',
    "blockCommentStart" : "/*",
    "blockCommentEnd" : "*/",
    "destFlag" : 'destdir',
    "fileExt" : '.java'
}
