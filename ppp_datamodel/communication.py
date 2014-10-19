"""Contains the classes representing a request to and a response of a module."""

import json

from .abstractnode import register, AbstractNode

class Request:
    """Represents a request.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#request
    """
    __slots__ = ('language', 'sentence', 'tree')

    def __init__(self, language, tree=None, sentence=None):
        assert tree or sentence
        self.sentence = sentence
        if isinstance(tree, dict) or isinstance(tree, str):
            tree = AbstractNode.from_json(tree)
        self.tree = tree
        self.language = language

    def __repr__(self):
        return '<PPP request language=%r, tree=%r, sentence=%r>' % \
                (self.language, self.tree, self.sentence)

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False
        return self.language == other.language and \
                self.tree == other.tree and \
                self.sentence == other.sentence

    @staticmethod
    def from_json(data):
        if isinstance(data, str):
            data = json.loads(data)
        if 'tree' not in data and 'sentence' not in data:
            raise KeyError("'tree' or 'sentence'")
        return Request(data['language'],
                       data.get('tree', None),
                       data.get('sentence', None))


    def as_dict(self):
        d = {'language': self.language}
        if self.tree:
            d['tree'] = self.tree.as_dict()
        if self.sentence:
            d['sentence'] = self.sentence.as_dict()
        return d
    def as_json(self):
        return json.dumps(self.as_dict())

class Response:
    """Represents a response.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#response
    """
    __slots__ = ('language', 'pertinence', 'tree')

    def __init__(self, language, pertinence, tree):
        if isinstance(tree, dict) or isinstance(tree, str):
            tree = AbstractNode.from_json(tree)
        self.language = language
        self.pertinence = pertinence
        self.tree = tree

    def __repr__(self):
        return '<PPP response language=%r, pertinence=%r, tree=%r>' % \
                (self.language, self.pertinence, self.tree)

    def __eq__(self, other):
        if not isinstance(other, Response):
            return False
        return self.language == other.language and \
                self.pertinence == other.pertinence and \
                self.tree == other.tree

    @staticmethod
    def from_json(data):
        if isinstance(data, str):
            data = json.loads(data)
        return Response(data['language'], data['pertinence'], data['tree'])

    def as_dict(self):
        return {'language': self.language,
                'pertinence': self.pertinence,
                'tree': self.tree.as_dict()}
    def as_json(self):
        return json.dumps(self.as_dict())
