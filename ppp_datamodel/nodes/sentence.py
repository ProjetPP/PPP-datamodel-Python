"""Contains the class representing a sentence leaf."""

from .abstractnode import register, AbstractNode

@register
class Sentence(AbstractNode):
    """Represents a sentence before it is parsed.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#sentence
    """
    __slots__ = ()
    _type = 'sentence'
    _possible_attributes = ('value',)


