"""Contains the class representing a resource leaf."""

from .abstractnode import register, AbstractNode

@register
class Resource(AbstractNode):
    """Represents a resource.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#resource
    """
    __slots__ = ()
    _type = 'resource'
    _possible_attributes = ('value',)

