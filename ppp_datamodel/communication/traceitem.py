import json

from ..nodes import AbstractNode

class TraceItem:
    """Represents a trace item.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#format-of-a-trace-item
    """
    __slots__ = ('module', 'tree', 'measures')

    def __init__(self, module, tree, measures):
        self.module = module
        self.tree = tree
        self.measures = measures

    @classmethod
    def from_json(cls, data):
        assert isinstance(data, str)
        data = json.loads(data)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        assert isinstance(data, dict)
        return cls(data['module'],
                   AbstractNode.from_dict(data['tree']),
                   data['measures'])

    def as_dict(self):
        return {'module': self.module,
                'tree': self.tree.as_dict(),
                'measures': self.measures,
               }

    def __repr__(self):
        return '<PPP traceitem module=%r, tree=%r, measures=%r>' % \
                (self.module, self.tree, self.measures)

    def __eq__(self, other):
        return self.module == other.module and \
                self.tree == other.tree and \
                self.measures == other.measures

    def __hash__(self):
        return hash((self.module, self.tree, self.measures))
