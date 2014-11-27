"""Contains operators that work on lists."""

from .abstractnode import register, AbstractNode

class ListOperator(AbstractNode):
    """Base class for list operators.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#union-intersection-and-or-first-and-last
    """
    __slots__ = ()
    _possible_attributes = ('list',)

    def _check_attributes(self, attributes):
        super(ListOperator, self)._check_attributes(attributes)
        if not isinstance(attributes['list'], list):
            raise TypeError('The “list” argument of the %s constructor '
                            'should be a list, not %r' %
                            (self.__class__.__name__, attributes['list']))

    def _parse_attributes(self, attributes):
        L = attributes['list']
        L = [x if isinstance(x, list) else [x] for x in L]
        attributes['list'] = L
        super(ListOperator, self)._parse_attributes(attributes)

class PredicateListOperator(ListOperator):
    __slots__ = ()
    _possible_attributes = ('list', 'predicate')


@register
class Union(ListOperator):
    __slots__ = ()
    _type = 'union'
@register
class Intersection(ListOperator):
    __slots__ = ()
    _type = 'intersection'
@register
class And(ListOperator):
    __slots__ = ()
    _type = 'and'
@register
class Or(ListOperator):
    __slots__ = ()
    _type = 'or'
@register
class First(ListOperator):
    __slots__ = ()
    _type = 'first'
@register
class Last(ListOperator):
    __slots__ = ()
    _type = 'last'

@register
class Sort(PredicateListOperator):
    __slots__ = ()
    _type = 'sort'
