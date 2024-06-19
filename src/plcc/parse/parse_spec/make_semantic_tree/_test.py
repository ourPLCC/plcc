from pytest import raises, fixture, mark


from . import make_semantic_tree
from . import SemanticTree, Block
from ...read_sections import Line


def test_None():
    assert make_semantic_tree(None) == SemanticTree(blocks=[])


def test_empty():
    assert make_semantic_tree('') == SemanticTree(blocks=[])


def test_blank_lines():
    given = '''



    '''

    make_semantic_tree(given) == SemanticTree(blocks=[])



def test_comment_lines():
    given = '''

        # comment

    '''

    make_semantic_tree(given) == SemanticTree(blocks=[])


@mark.skip
def test_default_block():
    given = '''

Hi
%%%
whatever
%%%

    '''

    assert make_semantic_tree(given) == SemanticTree(
        blocks=[
            Block(
                module='Hi',
                location='end_of_class',
                code=[
                    Line(string='whatever', number=5, file=None)
                ],
                line=Line(string='Hi', number=3, file=None)
            )
        ]
    )
