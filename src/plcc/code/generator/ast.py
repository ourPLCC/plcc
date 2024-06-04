from ..class_ import Class
from ..module import Module


class AstDesigner:
    def design(self, bnfspec):
        if not bnfspec:
            return []
        if not list(bnfspec.getRules()):
            return []
        print(bnfspec.getRules())
        return [Module()]
