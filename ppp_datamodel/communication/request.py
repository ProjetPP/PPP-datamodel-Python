import json

from .traceitem import TraceItem
from ..nodes import AbstractNode

class Request:
    """Represents a request.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#request
    """
    __slots__ = ('id', 'language', 'tree', 'measures', 'trace')

    def __init__(self, id, language, tree, measures={}, trace=[]):
        self.id = id
        assert isinstance(tree, str) or isinstance(tree, AbstractNode)
        self.tree = tree
        self.language = language
        self.measures = measures
        self.trace = [x if isinstance(x, TraceItem) else TraceItem.from_dict(x)
                      for x in trace]

    def __repr__(self):
        return '<ppp_datamodel.Request(%s)>' % \
                ', '.join(map(lambda x:'%s=%r' % (x, getattr(self, x)),
                              self.__slots__))

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False
        return self.id == other.id and \
                self.language == other.language and \
                self.tree == other.tree

    def __hash__(self):
        return hash((self.id, self.language, self.tree, self.trace))

    @classmethod
    def from_json(cls, data):
        assert isinstance(data, str)
        data = json.loads(data)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        assert isinstance(data, dict)
        tree = data['tree']
        if isinstance(tree, dict):
            tree = AbstractNode.from_dict(tree)
        return cls(data['id'],
                   data['language'],
                   tree,
                   data['measures'],
                   data['trace'])


    def as_dict(self):
        tree = self.tree
        if isinstance(tree, AbstractNode):
            tree = tree.as_dict()
        d = {'id': self.id, 'language': self.language,
             'measures': self.measures,
             'trace': [x.as_dict() for x in self.trace],
             'tree': tree}
        return d
    def as_json(self):
        return json.dumps(self.as_dict())
