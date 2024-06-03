from ..translator.code import Class
from ..translator.code import File


class AstDesigner:
    def design(self, bnfspec):
        if not bnfspec:
            return []
        if not list(bnfspec.getRules()):
            return []
        print(bnfspec.getRules())
        return [File()]
