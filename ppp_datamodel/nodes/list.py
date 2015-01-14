"""Contains the class representing a triple node."""

from .abstractnode import register, AbstractNode
from .resource import Resource

@register
class List(AbstractNode):
    """Represents a list.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#list-1
    """
    __slots__ = ()
    _type = 'list'
    _possible_attributes = ('list',)

    def _check_attributes(self, attributes):
        super(List, self)._check_attributes(attributes)
        if not isinstance(attributes['list'], list):
            raise TypeError('The “list” argument of the List constructor '
                            'should be a list, not %r' % attributes['list'])

    def _parse_attributes(self, attributes):
        L = attributes['list']
        L = [AbstractNode.from_dict(x) if isinstance(x, dict) else x
             for x in L]
        assert all(isinstance(x, Resource) for x in L), L
        attributes['list'] = L
        super(List, self)._parse_attributes(attributes)

    def __hash__(self):
        return hash(tuple(self.list))

    def as_dict(self):
        return {'type': self.type, 'list': [x.as_dict() for x in self.list]}

    def traverse(self, predicate):
        return predicate(self.__class__([x.traverse(predicate)
                                         for x in self.list]))
