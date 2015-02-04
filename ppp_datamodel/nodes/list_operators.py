"""Contains operators that work on lists."""

from .abstractnode import register, AbstractNode
from .resource import Resource
from .list import List

def to_abstract_node(x):
    assert isinstance(x, (AbstractNode, dict)), x
    return x if isinstance(x, AbstractNode) else AbstractNode.from_dict(x)

class ListNodeOperator(AbstractNode):
    """Base class for list operators.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#union-intersection-and-or-first-and-last
    """
    __slots__ = ()
    _possible_attributes = ('list',)

    def _check_attributes(self, attributes):
        super(ListNodeOperator, self)._check_attributes(attributes)
        if not isinstance(attributes['list'], AbstractNode):
            raise TypeError('The “list” argument of the %s constructor '
                            'should be a node, not %r' %
                            (self.__class__.__name__, attributes['list']))

    def traverse(self, predicate):
        if isinstance(self.list, List) or not isinstance(self.list, Resource):
            L = self.list
        else:
            L = List([self.list])
        return predicate(self.__class__(L.traverse(predicate)))

class ListOperator(AbstractNode):
    """Base class for list operators.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#union-intersection-and-or-first-and-last
    """
    __slots__ = ()
    _possible_attributes = ('list',)

    def _check_attributes(self, attributes):
        super(ListOperator, self)._check_attributes(attributes)
        if not hasattr(attributes['list'], '__iter__'):
            raise TypeError('The “list” argument of the %s constructor '
                            'should be an iterable, not %r' %
                            (self.__class__.__name__, attributes['list']))

    def _parse_attributes(self, attributes):
        L = attributes['list']
        assert hasattr(L, '__iter__') and not isinstance(L, AbstractNode)
        if all(isinstance(x, dict) for x in L):
            pass
        else:
            assert not any(isinstance(x, dict) for x in L)
        L = tuple(to_abstract_node(l) for l in L)
        attributes['list'] = L
        super(ListOperator, self)._parse_attributes(attributes)

    def as_dict(self):
        d = super().as_dict()
        d['list'] = [x.as_dict() for x in self.list]
        return d

    def traverse(self, predicate):
        return predicate(self.__class__([x.traverse(predicate)
                                         for x in self.list]))

class PredicateListOperator(ListNodeOperator):
    __slots__ = ()
    _possible_attributes = ('list', 'predicate')

    def _check_attributes(self, attributes):
        super()._check_attributes(attributes)
        if not isinstance(attributes['predicate'], Resource):
            raise TypeError('predicate should be a Resource, not %r' %
                    attributes['predicate'])
    def traverse(self, predicate):
        if isinstance(self.list, List) or not isinstance(self.list, Resource):
            L = self.list
        else:
            L = List([self.list])
        return predicate(self.__class__(
                list=L.traverse(predicate),
                predicate=self.predicate.traverse(predicate)))


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
class First(ListNodeOperator):
    __slots__ = ()
    _type = 'first'
@register
class Last(ListNodeOperator):
    __slots__ = ()
    _type = 'last'
@register
class Exists(ListNodeOperator):
    __slots__ = ()
    _type = 'exists'

@register
class Sort(PredicateListOperator):
    __slots__ = ()
    _type = 'sort'
