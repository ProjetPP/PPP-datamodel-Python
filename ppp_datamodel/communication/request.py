import json

from .traceitem import TraceItem
from ..nodes import AbstractNode
from .traceitem import TraceItem
from ..utils import SerializableAttributesHolder

class Request(SerializableAttributesHolder):
    """Represents a request.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#request
    """
    __slots__ = ()
    _possible_attributes = ('id', 'language', 'tree', 'measures', 'trace')

    def _check_attributes(self, attributes, extra=None):
        super(Request, self)._check_attributes(attributes)
        assert {'id', 'language', 'tree'}.issubset(set(attributes.keys())), \
                (attributes, extra)
        assert isinstance(attributes['tree'], (str, AbstractNode))
        assert isinstance(attributes['language'], str)
        assert isinstance(attributes['tree'], AbstractNode)
        assert isinstance(attributes['measures'], dict)
        assert isinstance(attributes['trace'], list)

    def _parse_attributes(self, attributes):
        attributes['measures'] = attributes.get('measures', {})
        attributes['trace'] = \
                [x if isinstance(x, TraceItem) else TraceItem.from_dict(x)
                 for x in attributes.get('trace', [])]
        super(Request, self)._parse_attributes(attributes)

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False
        else:
            return super(Request, self).__eq__(other)

    def __hash__(self):
        return hash((Request, self._attributes))

    @classmethod
    def deserialize_attribute(cls, key, value):
        if key == 'tree':
            return AbstractNode.deserialize_attribute(key, value)
        elif key == 'trace':
            return [TraceItem.from_dict(x) for x in value]
        else:
            return value
