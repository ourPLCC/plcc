from dataclasses import dataclass
from plcc.load_spec.load_rough_spec.parse_lines import Line
import re

@dataclass
class TargetLocator:
    line: Line
    className: str
    modifier: str = None

def parse_target_locator(line, regex=r'^(.+?)(?::([a-z]+))?\s*(?:#.*)?$'):
    match = re.match(regex, line.string)
    if match:
        name, modifier = match.group(1), match.group(2) or None
        return TargetLocator(line = line, className=name, modifier=modifier)
    raise InvalidTargetLocatorError(line)

class InvalidTargetLocatorError(Exception):
    def __init__(self, line):
        self.line = line
