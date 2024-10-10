from dataclasses import dataclass
import re


from .parse_lines import Line


@dataclass
class Divider:
    tool: str
    language: str
    line: Line

def parse_dividers(lines: list[Line], tool='Java', language='Java') -> list[Divider | Line]:
    return DividerParser(lines, tool, language).parse()

class DividerParser:
    def __init__(self, lines: list[Line], tool="Java", language="Java"):
        self.lines = lines
        self.defaultTool = tool
        self.defaultLanguage = language
        self.patterns = self._compilePatterns()

    def parse(self):
        if not self.lines:
            return
        for line in self.lines:
            yield self._parseDividerLine(line) if self._isLineObject(line) and self._isDividerLine(line.string) else line

    def _parseDividerLine(self,line) -> Divider:
        matchToolLanguage = self._matchToolLanguage(line.string)
        matchToolOnly = self._matchToolOnly(line.string)
        tool = self._getTool(matchToolLanguage, matchToolOnly)
        language = self._getLanguage(matchToolLanguage, matchToolOnly)
        return self._createDivider(tool, language, line)

    def _getTool(self, matchToolLanguage, matchToolOnly) -> str:
        if matchToolLanguage:
            return matchToolLanguage['tool']
        elif matchToolOnly:
            return matchToolOnly['tool']
        else:
            return self.defaultTool

    def _getLanguage(self, matchToolLanguage, matchToolOnly) -> str:
        if matchToolLanguage:
            return matchToolLanguage['language']
        elif matchToolOnly:
            return matchToolOnly['tool']
        else:
            return self.defaultLanguage

    def _isLineObject(self, line: Line) -> bool:
        return isinstance(line,Line)

    def _isDividerLine(self, lineStr: str) -> bool:
        return bool(self.patterns['divider'].match(lineStr))

    def _matchToolLanguage(self, lineStr: str):
        return self.patterns['toolLanguage'].match(lineStr)

    def _matchToolOnly(self, lineStr):
        return self.patterns['toolOnly'].match(lineStr)

    def _createDivider(self, tool: str, language: str, line: Line) -> Divider:
        return Divider(tool=tool, language=language, line=line)

    def _compilePatterns(self) -> dict:
        return {
            'divider': re.compile(r'^%(?:\s.*)?$'),
            'toolLanguage': re.compile(r'^%\s*(?P<tool>\S+)\s(?P<language>\S+).*$'),
            'toolOnly': re.compile(r'^%\s*(?P<tool>\S+)\s*$')
        }


