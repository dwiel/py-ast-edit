import ast, asttokens
import compute_input

source = """import compute_input

def test_f():
    compute_input.f('x = 1')
    assert x == 5

"""

def test_f():
    tree = ast.parse(source)
    tokens = asttokens.ASTTokens(source, tree=tree)
    tokens.mark_tokens(tree)

    node = compute_input.node(tree, 3, 5)
    print '-'
    print node
    print node.parent
    assert False
