
class ConcreteParserMethod:
    def __init__(self):
        self._lhs = None
        self._body = None

    def initLhs(self, lhs):
        self._lhs = lhs

    def initBody(self, body):
        self._body = body

    def compose(cls, lhs, body):
        return f'''\
    public static {cls} parse(Scan scn$, Trace trace$) {{
        if (trace$ != null)
            trace$ = trace$.nonterm("{lhs}", scn$.lno);
{body}
    }}
'''
