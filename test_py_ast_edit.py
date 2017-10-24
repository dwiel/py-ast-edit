import ast, asttokens
import compute_input

source = """import compute_input

def test_f():
    compute_input.f('x = 1')
    assert x == 5

"""


def test_node():
    tree = ast.parse(source)
    tokens = asttokens.ASTTokens(source, tree=tree)
    tokens.mark_tokens(tree)

    node = compute_input.nodes(tree, 3, 5)[-1]
    assert type(node).__name__ == 'Name'


def test_node_empty_line():
    tree = ast.parse(source)
    tokens = asttokens.ASTTokens(source, tree=tree)
    tokens.mark_tokens(tree)

    node = compute_input.nodes(tree, 1, 5)[-1]
    assert type(node).__name__ == 'Module'
