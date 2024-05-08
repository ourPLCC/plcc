
def parseSections(specLines):
    return SectionParser().getSections(specLines)


class SectionParser():
    def __init__(self):
        self._isInCodeBlock = False

    def getSections(self, lines):
        section = []
        for line in lines:
            if self._isEndOfSection(line):
                yield section
                section = []
            elif self._isStartOfCodeBlock(line):
                self._startCodeBlock()
            elif self._isEndOfCodeBlock(line):
                self._endCodeBlock()
            section.append(line)
        yield section

    def _isEndOfSection(self, line):
        return not self._isInCodeBlock and line == '%'

    def _isStartOfCodeBlock(self, line):
        return not self._isInCodeBlock and line in ['%%%', '%%{']

    def _isEndOfCodeBlock(self, line):
        return self._isInCodeBlock and line in ['%%%', '%%}']

    def _startCodeBlock(self):
        self._isInCodeBlock = True

    def _endCodeBlock(self):
        self._isInCodeBlock = False
