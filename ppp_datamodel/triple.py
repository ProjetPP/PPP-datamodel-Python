"""Contains the class representing a triple."""

from .abstractnode import TYPE_TO_CLASS, AbstractNode

class Triple(AbstractNode):
    """Represents a triple.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#triple
    """
    _type = 'triple'
    _possible_attributes = ('subject', 'predicate', 'object')

TYPE_TO_CLASS['triple'] = Triple
