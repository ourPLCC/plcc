import re


class LexValidator:
    def validate(self, lexrules):
        self.namesAreUppercaseAndUnderscoreOnly(lexrules)
        self.noDuplicateNames(lexrules)

    def namesAreUppercaseAndUnderscoreOnly(self, lexrules):
        uppersAndUnderscore = re.compile(r'^[A-Z_]+$')
        for rule in lexrules:
            if not uppersAndUnderscore.match(rule.name):
                raise self.InvalidName(rule.line)

    def noDuplicateNames(self, lexrules):
        names = set()
        for r in lexrules:
            if r.name in names:
                raise self.DuplicateName(r.line)
            names.add(r.name)

    class InvalidName(Exception):
        pass

    class DuplicateName(Exception):
        pass
