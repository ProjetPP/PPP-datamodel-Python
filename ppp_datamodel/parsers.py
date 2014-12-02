"""Contains a parser for the “human-writable” notation of the datamodel."""

import collections

from .nodes import List, Triple, Missing, Resource, Or, And, Intersection, Union

__all__ = ['ParseError', 'parse_triples']

class ParseError(Exception):
    pass

OPERATORS = ('[', ']', '(', ')', ',', '/\\', r'\\/')
def lex_triples(sentence):
    buff = ''
    for char in sentence:
        buff += char
        operators = list(filter(buff.endswith, OPERATORS))
        if operators:
            assert len(operators) == 1, operators
            op = operators[0]
            last_token = buff[0:-len(op)]
            if last_token.strip():
                yield last_token.strip()
            buff = ''
            yield op
    if buff.strip():
        yield buff.strip()

stackitem = collections.namedtuple('stackitem', 'type tree')
TYPES = {
        '(': 'paren', ')': 'paren',
        '[': 'brack', ']': 'brack',
        }
OPEN = '(['
CLOSE = ')]'
def parse_forest(tokens):
    forest = []
    stack = [stackitem('root', forest)]
    for token in tokens:
        type_ = TYPES.get(token, None)
        if token in OPEN:
            stack.append(stackitem(type_, []))
            stack[-2].tree.append(stack[-1])
        elif token in CLOSE:
            if stack[-1].type == 'root':
                raise ParseError('Stack is empty')
            elif stack[-1].type != type_:
                raise ParseError('Overlapping parenthesing')
            stack.pop(-1)
        elif token == ',':
            pass
        elif token in ('\\/', '/\\'):
            stack[-1].tree.append(stackitem('operator', token))
        else:
            stack[-1].tree.append(stackitem('resource', token))
    if stack[-1].type != 'root':
        raise ParseError('Stack is not empty')
    return forest


OPERATOR_TO_CLASS = {
        '\\/': Or, '∨': Or,
        '/\\': And, '∧': And,
        '∪': Union,
        '∩': Intersection,
        }
def make_operators(lists):
    operators = lists[1::][::2] # Odd
    items = lists[::2] # Even
    if len(lists) % 2 != 1 or \
            any(x.tree not in OPERATOR_TO_CLASS for x in operators):
        raise ParseError('Juxtaposition of items.')
    op = operators[0]
    if any(x != op for x in operators):
        raise ParseError('All operators at same level should be the same.')
    cls = OPERATOR_TO_CLASS[op.tree]
    return cls(list(map(make_triples, items)))
def make_triples(lists):
    if not isinstance(lists, stackitem):
        assert isinstance(lists, list), lists
        if len(lists) == 1:
            # This is “priority parenthesing”
            return make_triples(lists[0])
        else:
            return make_operators(lists)
    elif lists.type == 'resource':
        if lists.tree == '?':
            return Missing()
        else:
            return Resource(value=lists.tree)
    elif lists.type == 'paren':
        if len(lists.tree) == 1:
            return make_triples(lists.tree[0])
        elif len(lists.tree) == 3 and \
                all(x.type != 'operator' for x in lists.tree):
            return Triple(*map(make_triples, lists.tree))
        else:
            return make_triples(lists.tree)
    elif lists.type == 'brack':
        return List(list(map(make_triples, lists.tree)))
    else:
        assert False, lists



def parse_triples(sentence):
    return make_triples(parse_forest(lex_triples(sentence)))

