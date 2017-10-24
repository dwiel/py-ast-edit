import sys, json
import asttokens, ast


def read_in():
    return ''.join(sys.stdin.readlines())


def position_python_to_atom(position):
    return (position[0] - 1, position[1])


def nodes(tree, query_line_number, query_column_offset):
    # todo: doesn't work when query is in symbols
    query_line_number += 1

    cursor_position = (query_line_number, query_column_offset)

    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    results = []
    last_node = None
    for node in ast.walk(tree):
        first_token = getattr(node, 'first_token', None)
        last_token = getattr(node, 'last_token', None)
        if first_token and first_token.start <= cursor_position:
            if last_token.end >= cursor_position:
                # print node, node.first_token.start, node.last_token.end
                results.append(node)

    return results


def range_atom_to_python(range):
    return (range['row'], range['column'])


def select_parent(data, source):
    if 'selected_range' in data:
        data['selected_range']['start'] = range_atom_to_python(data['selected_range']['start'])
        data['selected_range']['end'] = range_atom_to_python(data['selected_range']['end'])

        cursor_position = data['selected_range']['start']
    else:
        cursor_position = range_atom_to_python(data['cursor_position'])

    # print 'data', data

    tree = ast.parse(source)
    tokens = asttokens.ASTTokens(source, tree=tree)
    tokens.mark_tokens(tree)

    last_node = nodes(tree, *cursor_position)[-1]

    for _ in range(30):
        last_node = last_node.parent

        token_list = list(tokens.get_tokens(last_node))
        selection_range = {
            'start': position_python_to_atom(min(token.start for token in token_list)),
            'end': position_python_to_atom(max(token.end for token in token_list)),
        }

        # print selection_range
        # print data['selected_range']
        # print '~'

        if selection_range['start'] != data['selected_range']['start']:
            break
        if selection_range['end'] > data['selected_range']['end']:
            # current range found is larger than already selected range
            break

    return selection_range


def main():
    data = sys.stdin.readline()
    data = json.loads(data)

    print json.dumps(select_parent(data, read_in()))

    # TODO: cell assign|function|method|class|argument
    # TODO: kill *
    # TODO: go *
    # TODO: cell [prev|next] [arg|class|assign]
    # TODO: arg, class, function, import, print, assert, statement, comprehension, slice, index, attribute, if_expression, call, compare, if, for, while, break, loop, try, ...
    # TODO: cell bro, cousin prev/next

if __name__ == '__main__':
    main()
