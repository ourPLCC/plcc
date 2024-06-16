import re

class SectionParser:
    def __init__(self, builder):
        self.builder = builder
        self.codeBrackets = {
            '%%%': '%%%',
            '%%{': '%%}',
        }

    def parse(self, lines):
        isStarted = False
        codeClosing = None
        for line in lines:
            if not isStarted:
                self.builder.start()
                isStarted = True
            if not codeClosing and line.string in self.codeBrackets:
                codeClosing = self.codeBrackets[line.string]
                self.builder.openCode(line)
            elif codeClosing and line.string == codeClosing:
                codeClosing = None
                self.builder.closeCode(line)
            elif codeClosing:
                self.builder.codeLine(line)
            elif line.string == '%':
                self.builder.divider(line)
            else:
                self.builder.line(line)

