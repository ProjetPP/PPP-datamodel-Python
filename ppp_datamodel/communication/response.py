import json

from ..nodes import AbstractNode
from .traceitem import TraceItem

class Response:
    """Represents a response.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#response
    """
    __slots__ = ('language', 'tree', 'measures', 'trace')

    def __init__(self, language, tree, measures, trace):
        if isinstance(tree, dict):
            tree = AbstractNode.from_dict(tree)
        elif isinstance(tree, str):
            tree = AbstractNode.from_json(tree)
        self.language = language
        self.measures = measures
        self.tree = tree
        self.trace = [x if isinstance(x, TraceItem) else TraceItem.from_dict(x)
                      for x in trace]

    def __repr__(self):
        return '<PPP response language=%r, tree=%r, measures=%r, trace=%r>'%\
                (self.language, self.tree, self.measures, self.trace)

    def __eq__(self, other):
        if not isinstance(other, Response):
            return False
        return self.language == other.language and \
                self.tree == other.tree and \
                self.measures == other.measures and \
                self.trace == other.trace

    def __hash__(self):
        return hash((self.language, self.tree, self.measures, self.trace))

    @classmethod
    def from_json(cls, data):
        data = json.loads(data)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        return cls(data['language'], data['tree'], data['measures'],
                   list(map(TraceItem.from_dict, data['trace'])))

    def as_dict(self):
        return {'language': self.language,
                'tree': self.tree.as_dict(),
                'measures': self.measures,
                'trace': [x.as_dict() for x in self.trace]
               }
    def as_json(self):
        return json.dumps(self.as_dict())
