from typing import Iterable


from ..specfiles.lines import Line


def Spec():
    def parse(self, lines: Iterable[Line]):
        ...

    def getSectionCount(self):
        return 3
