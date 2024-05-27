import re


from .semrule import SemRule


class SemParser:
    def __init__(self):
        self._classPattern=re.compile(r'^\s*(?P<class_>\w+)(?::(?P<modifier>\w+))?(?:\s*#.*)?$')

    def parseIntoSemSpec(self, lines):
        return SemSpec(list(self.parseIntoSemRules()))

    def parseIntoSemRules(self, lines):
        for line in lines:
            m = self._classPattern.match(line.string)
            if not m:
                raise self.InvalidSemRule()
            next(lines)
            line = next(lines)
            codeBlock = []
            while line.isInCodeBlock:
                codeBlock.append(line)
                line = next(lines)
            yield SemRule(class_=m['class_'], modifier=m['modifier'], code=codeBlock)

    class InvalidSemRule(Exception):
        pass
