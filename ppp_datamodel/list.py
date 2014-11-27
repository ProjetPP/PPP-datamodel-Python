"""Contains the class representing a triple node."""

from .abstractnode import register, AbstractNode

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
        L = [AbstractNode.from_dict(x) for x in L]
        attributes['list'] = L
        super(List, self)._parse_attributes(attributes)
