"""Contains the class representing a “missing” leaf."""

from .abstractnode import register, AbstractNode

@register
class Missing(AbstractNode):
    """Represents a “missing” node.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#missing
    """
    __slots__ = ()
    _type = 'missing'
    _possible_attributes = ()

