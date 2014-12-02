from .nodes import Triple, Resource, Missing

class ParseError(Exception):
    pass

def lex_triples(sentence):
    token = ''
    for char in sentence:
        if char in '(),':
            if token.strip():
                yield token.strip()
                token = ''
            yield char
        else:
            token += char
def parse_forest(tokens):
    forest = []
    stack = [forest]
    for token in tokens:
        if token == '(':
            stack.append([])
            stack[-2].append(stack[-1])
        elif token == ')':
            if len(stack) == 1:
                raise ParseError('Stack is empty')
            stack.pop(-1)
        elif token == ',':
            pass
        else:
            stack[-1].append(token)
    if len(stack) > 1:
        raise ParseError('Stack is not empty')
    return forest
def make_triples(lists):
    if isinstance(lists, str):
        if lists[0] == '?':
            return Missing()
        else:
            return Resource(value=lists)
    else:
        assert isinstance(lists, list)
        if len(lists) == 3:
            return Triple(*map(make_triples, lists))
        else:
            raise ParseError('“Triple” of size %d: %r' % (len(lists), lists))



def parse_triples(sentence):
    return list(map(make_triples, parse_forest(lex_triples(sentence))))

