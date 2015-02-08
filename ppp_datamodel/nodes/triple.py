"""Contains the class representing a triple node."""

from .abstractnode import register, AbstractNode
from .list import List

@register
class Triple(AbstractNode):
    """Represents a triple.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#triple
    """
    __slots__ = ()
    _type = 'triple'
    _possible_attributes = ('subject', 'predicate', 'object')

    def _check_attributes(self, attributes):
        super(Triple, self)._check_attributes(attributes)
        if not all(isinstance(x, AbstractNode) for x in attributes.values()):
            raise TypeError('One of Triple\'s constructor argument '
                            'is not an AbstractNode instance.')

    @property
    def predicate_set(self):
        """Return a frozenset of predicates, extracting it from the list
        if it is a List node."""
        if isinstance(self.predicate, List):
            return frozenset(self.predicate.list)
        else:
            return frozenset({self.predicate})
