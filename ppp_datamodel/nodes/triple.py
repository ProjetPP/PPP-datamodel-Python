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
    _possible_attributes = ('subject', 'predicate', 'object', 'inverse_predicate')

    def _check_attributes(self, attributes):
        attributes['inverse_predicate'] = \
                attributes.get('inverse_predicate', List([]))
        super(Triple, self)._check_attributes(attributes)
        if not all(isinstance(x, AbstractNode) for x in attributes.values()):
            raise TypeError('One of Triple\'s constructor argument '
                            'is not an AbstractNode instance.')

    def as_dict(self):
        """Do not put inverse-predicate in the output dict if it
        is an empty list."""
        d = super().as_dict()
        if d['inverse-predicate']['type'] == 'list' and \
                d['inverse-predicate']['list'] == []:
            del d['inverse-predicate']
        return d

    @property
    def predicate_set(self):
        """Return a frozenset of predicates, extracting it from the list
        if it is a List node."""
        if isinstance(self.predicate, List):
            return frozenset(self.predicate.list)
        else:
            return frozenset({self.predicate})

    @property
    def inverse_predicate_set(self):
        """Return a frozenset of inverse predicates, extracting it from the list
        if it is a List node."""
        if isinstance(self.inverse_predicate, List):
            return frozenset(self.inverse_predicate.list)
        else:
            return frozenset({self.inverse_predicate})
