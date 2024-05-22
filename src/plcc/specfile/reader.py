from __future__ import annotations
from dataclasses import dataclass, replace
import pathlib
import re


from .line import Line


class SpecFileReaderPatterns:
    def __init__(self):
        self.sectionSeparator = re.compile(r'^%$')
        self.brackets = {
            '%%%': '%%%',
            '%%{': '%%}'
        }
        self.comment = re.compile(r'#.*')
        self.include = re.compile(r'^%include\s+(?P<path>.*)$')


class SpecFileReader:
    def __init__(self, specFilePatterns = None):
        if specFilePatterns is None:
            specFilePatterns = SpecFileReaderPatterns()
        self._patterns = specFilePatterns

    def readSectionsFromSpecFile(self, pathStr):
        return self.groupLinesIntoSections(self.readLinesFromSpecFile(pathStr))

    def groupLinesIntoSections(self, lines):
        sections = []
        section = []
        sections.append(section)
        for line in lines:
            if self._patterns.sectionSeparator.match(line.string.strip()):
                section = []
                sections.append(section)
            else:
                section.append(line)
        return sections

    def readLinesFromString(self, string):
        lines = self.splitStringIntoLines(string)
        return self.processLines(lines)

    def splitStringIntoLines(self, string):
        for number, lineStr in enumerate(string.splitlines(), start=1):
            yield Line(path='', number=number, string=lineStr, isInBlock=False)

    def readLinesFromSpecFile(self, pathStr):
        lines = self.readLinesFromFile(pathStr)
        return self.processLines(lines, pathStr)

    def readLinesFromFile(self, pathStr):
        pathStr = self.resolveRelativePath(pathStr, pathlib.Path.cwd())
        path = pathlib.Path(pathStr).resolve()
        pathStr = str(pathStr)
        with path.open(mode='r') as file:
            for number, line in enumerate(file, start=1):
                yield Line(pathStr,number,line.rstrip())

    def processLines(self, lines, pathStr=''):
        lines = self.markBlocks(lines)
        lines = self.ignoreCommentLines(lines)
        lines = self.ignoreBlankLines(lines)
        lines = self.processIncludes(lines, sourceFilePathStr=pathStr)
        return lines

    def markBlocks(self, lines):
        isInBlock = False
        close = None

        def mark(line):
            nonlocal isInBlock
            nonlocal close

            s = line.string.strip()
            if not close:
                if s in self._patterns.brackets:
                    close = self._patterns.brackets[s]
            elif s == close:
                close = None
            else:
                line = line.markIsInBlock()
            return line

        return map(mark, lines)

    def ignoreCommentLines(self, lines):
        def isComment(line):
            s = line.string.strip()
            return not line.isInBlock and s and self._patterns.comment.match(s)
        return filter(lambda line: not isComment(line), lines)

    def ignoreBlankLines(self, lines):
        def isBlankLine(line):
            s = line.string.strip()
            return not line.isInBlock and not s
        return filter(lambda line: not isBlankLine(line), lines)

    def processIncludes(self, lines, sourceFilePathStr, stack=None):
        sourceFilePath = pathlib.Path(sourceFilePathStr).resolve()
        sourceDirPath = sourceFilePath.parent
        if stack is None:
            stack = [ str(sourceFilePath) ]
        for line in lines:
            if line.isInBlock:
                yield line
                continue
            m = self._patterns.include.match(line.string)
            if not m:
                yield line
                continue
            pathStr = self.resolveRelativePath(m['path'], str(sourceDirPath))
            if pathStr in stack:
                raise self.CircularIncludeException(line)
            stack.append(pathStr)
            yield from self.processIncludes(self.readLinesFromFile(pathStr), pathStr, stack)
            stack.pop()

    class CircularIncludeException(Exception):
        def __init__(self, line):
            self.line = line

    def resolveRelativePath(self, pathStr, basePathStr):
        path = pathlib.Path(pathStr)
        if path.is_absolute():
            return pathStr
        return str((pathlib.Path(basePathStr).resolve() / path).resolve())
