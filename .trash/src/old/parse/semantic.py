from .error import ParseError
from .line import Line


from ..spec.semantic import SemanticSpec


def parseSemanticSpec(lines, lexicalSpec, syntacticSpec):
    p = SemanticParser()
    p.initLexicalSpec(lexicalSpec)
    p.initSyntacticSpec(syntacticSpec)
    p.parse(lines)
    return p.getSemanticSpec()


class SemanticParser:
    def __init__(self):
        self._lexicalSpec = None
        self._syntacticSpec = None
        self._blocks = []

    def initLexicalSpec(self, lexicalSpec):
        self._lexicalSpec = lexicalSpec

    def initSyntacticSpec(self, syntacticSpec):
        self._syntacticSpec = syntacticSpec

    def parse(self, lines):
        lines = iter(lines)
        for line_obj in lines:
            line = line_obj.text
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                # skip comments or blank lines
                continue
            (cls, _, mod) = line.partition(':')
            cls = cls.strip()
            codeString = self._getCode(lines) # grab the stuff between %%% ... %%%
            if line[-8:] == ':ignore!':
                continue
            # check to see if line has the form Class:mod
            mod = mod.strip() # mod might be 'import', 'top', etc.
            self._blocks.add(Block(cls, mod, codeString, line_obj))

    def _getCode(self, lines):
        code = []
        offset = None
        for line_obj in lines:
            line = line_obj.text
            line = line.rstrip()
            if re.match(r'\s*#', line) or re.match(r'\s*$', line):
                # skip comments or blank lines
                continue
            if re.match(r'%%{', line): # legacy plcc
                stopMatch = r'%%}'
                break
            if re.match(r'%%%', line):
                stopMatch = r'%%%'
                break
            else:
                raise ParseError(line=line_obj, message='expecting a code segment')
        lineMode = True # switch on line mode
        for line_obj in lines:
            line = line_obj.text
            if re.match(stopMatch, line):
                break
            if offset == None:
                offset = self._getOffset(line)
            line = self._removeOffset(line, offset)
            code.append(line)
        else:
            raise ParseError(line=line_obj, message='premature end of file')
        lineMode = False # switch off line mode
        if len(code)>0 :
            while len(code[0]) == 0:
                code.pop(0)
            while len(code[-1]) == 0:
                code.pop()
        return code

    def _removeOffset(self, ln, offset):
        check = ln.strip()
        if len(check) == 0:
            return ln
        s = re.sub(offset,"",ln,count=1)
        return s

    def _getOffset(self, line):
        check = line.lstrip()
        if len(check) == 0 or check[0] == '#':
            return None
        s = re.search(r"\S", line).start()
        return line[0:s]

    def getSemanticSpec(self):
        spec = SemanticSpec()
        spec.initBlocks(self._blocks)
        return spec
