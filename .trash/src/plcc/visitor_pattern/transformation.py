class Transformation:
    '''
    Applies a visitor to each node a tree following a bottom-up traversal.
    The results of applying the visitor to each attribute of a node is passed
    to the visit_T(...) method as keyword arguments with the same name as
    the attributes.

    When lists are encountered, returns a new list with the results of visiting
    each element of the list.

    Example
        from dataclasses import dataclass
        from plcc.visitor_pattern import Transformation, Visitor

        @dataclass
        class A:
            bs: [B]

        @dataclass
        class B:
            m: str

        class Copy(Visitor):
            """Create a deep copy of tree."""

            def visit_A(self, bs):
                return A(bs)

            def visit_B(self, m):
                return B(m)

            def visit_Str(self, string):
                return str(string)

        copyMaker = Transformation(Copy())
        tree = A(B("hi"))
        newTree = copyMaker.visit(tree)
    '''
    def __init__(self, visitor):
        self.visitor = visitor

    def visit(self, obj):
        '''
        Apply visitor to each dataclass object, bottom up.
        Results from visiting a dataclass object's children are passed to the
        visit method as keyword arguments. For example if the dataclass object
        has fields x and y, then those fields are visited first and their
        results are passed to the visit call for the original object as
        keyword arguments x and y (roughly v.visit(o, x=v.visit(o.x), y=v.visit(o.y))).
        '''
        if is_dataclass(obj):
            d = {field.name: getattr(obj, field.name) for field in fields(obj)}
            visitedFields = {k: self.visit(d[k]) for k in d}
            return self.visitor.visit(obj, **visitedFields)
        elif isinstance(obj, list):
            return [self.visit(e) for e in obj]
        else:
            return obj
