"""Contains the classes representing a request to and a response of a module."""

from .abstractnode import register, AbstractNode

class Request:
    """Represents a request.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#request
    """
    __slots__ = ('language', 'pertinence', 'tree')

    def __init__(self, language, pertinence, tree):
        assert isinstance(tree, AbstractNode)
        assert 0 <= pertinence <= 1
        self.language = language
        self.tree = tree

    def __repr__(self):
        return '<PPP request language=%r, tree=%r>' % \
                (self._language, self._tree)

    def __eq__(self, other):
        return self.language == other.language and \
                self.tree == other.tree

class Response:
    """Represents a response.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#response
    """
    __slots__ = ('language', 'pertinence', 'tree')

    def __init__(self, language, pertinence, tree):
        assert isinstance(tree, AbstractNode)
        self.language = language
        self.pertinence = pertinence
        self.tree = tree

    def __repr__(self):
        return '<PPP response language=%r, pertinence=%r, tree=%r>' % \
                (self._language, self._pertinence, self._tree)

    def __eq__(self, other):
        return self.language == other.language and \
                self.pertinence == other.pertinence and \
                self.tree == other.tree
