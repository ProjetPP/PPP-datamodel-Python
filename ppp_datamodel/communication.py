"""Contains the classes representing a request to and a response of a module."""

import json

from .abstractnode import register, AbstractNode

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
        self.trace = trace

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
             'measures': self.measures, 'trace': self.trace,
             'tree': tree}
        return d
    def as_json(self):
        return json.dumps(self.as_dict())

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
