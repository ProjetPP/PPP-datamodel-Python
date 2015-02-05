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

    def predicate_among(self, L):
        # Be quite permissive about what we accept as L and convert it to
        # a (frozen)set.
        if isinstance(L, AbstractNode):
            L = frozenset({L})
        elif not isinstance(L, (set, frozenset)):
            pass
        elif hasattr(L, '__iter__'):
            L = frozenset(L)
        else:
            raise TypeError('%r is neither an interable or an AbstractNode.' %
                    L)

        # Check if any of the predicates is in L.
        if isinstance(self.predicate, List):
            return not frozenset(self.predicate.list).isdisjoint(L)
        else:
            return self.predicate in L
