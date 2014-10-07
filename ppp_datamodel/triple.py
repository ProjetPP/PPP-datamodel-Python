"""Contains the class representing a triple node."""

from .abstractnode import register, AbstractNode

@register
class Triple(AbstractNode):
    """Represents a triple.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#triple
    """
    _type = 'triple'
    _possible_attributes = ('subject', 'predicate', 'object')

