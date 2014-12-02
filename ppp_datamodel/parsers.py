"""Contains a parser for the “human-writable” notation of the datamodel."""

import collections

from .nodes import List, Triple, Missing, Resource

__all__ = ['ParseError', 'parse_triples']

class ParseError(Exception):
    pass

OPERATORS = ('[', ']', '(', ')', ',')
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

stackitem = collections.namedtuple('stackitem', 'type tree')
TYPES = {
        '(': 'triple', ')': 'triple',
        '[': 'list', ']': 'list',
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
        else:
            stack[-1].tree.append(stackitem('resource', token))
    if stack[-1].type != 'root':
        raise ParseError('Stack is not empty')
    return forest
def make_triples(lists):
    assert isinstance(lists, stackitem), lists
    if lists.type == 'resource':
        if lists.tree == '?':
            return Missing()
        else:
            return Resource(value=lists.tree)
    elif lists.type == 'triple':
        if len(lists.tree) == 3:
            return Triple(*map(make_triples, lists.tree))
        else:
            raise ParseError('“Triple” of size %d: %r' % (len(lists.tree), lists))
    elif lists.type == 'list':
        return List(list(map(make_triples, lists.tree)))
    else:
        assert False, lists



def parse_triples(sentence):
    return list(map(make_triples, parse_forest(lex_triples(sentence))))

