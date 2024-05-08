class ParseError(Exception):
    def __init__(self, line, message):
        self._line = line
        self._message = message
