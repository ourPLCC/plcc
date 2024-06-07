from plcc.code.render.default import Default


def test_default_indents_4_spaces_per_level():
    lines = ['one', 'two']

    result = Default().indentLines(lines, levels=1)
    for line in result:
        line.startswith(' ' * 4)

    result = Default().indentLines(lines, levels=2)
    for line in result:
        line.startswith(' ' * 8)
