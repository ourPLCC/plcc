spec = {
    "abstractStubFormatString" : """\
#{base}:top#
#{base}:import#

class {base}({ext}): #{base}:class#

    className = "{base}"

    #{base}#
""",

    "stubFormatString" : """\
#{cls}:top#
#{cls}:import#

# {ruleString}
class {cls}({ext}): #{cls}:class#

    className = "{cls}"
    ruleString = "{ruleString}"
{decls}

    def __init__({params}):
        #{cls}:init#
{inits}

#{cls}#
""",
    "extendFormatString" : '{cls}',
    "declFormatString" : '{field} = None',
    "initFormatString" : 'self.{field} = {field}',
    "paramFormatString" : '{field}',
    "semFlag" : 'python_semantics',
    "lineComment" : '#',
    "blockCommentStart" : "'''",
    "blockCommentEnd" : "'''",
    "destFlag" : 'python_destdir',
    "fileExt" : '.py'
}
