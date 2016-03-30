import sys
import json

from ..nodes import AbstractNode
from ..utils import SerializableAttributesHolder

if sys.version_info[0] >= 3:
    basestring = str

class TraceItem(SerializableAttributesHolder):
    """Represents a trace item.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#format-of-a-trace-item
    """
    __slots__ = ()
    _possible_attributes = ('module', 'tree', 'measures', 'times')

    def _check_attributes(self, attributes, extra=None):
        super(TraceItem, self)._check_attributes(attributes)
        # Allow missing 'time' attribute for now (transitioning)
        assert {'module', 'tree', 'measures'}.issubset(set(attributes.keys())),\
                (attributes, extra)
        assert isinstance(attributes['module'], basestring), module
        assert isinstance(attributes['tree'], AbstractNode)
        assert isinstance(attributes['measures'], dict)
        assert isinstance(attributes.get('times', {}), dict)

    def _parse_attributes(self, attributes):
        # Allow missing 'time' attribute for now (transitioning)
        attributes.setdefault('times', {})
        super(TraceItem, self)._parse_attributes(attributes)

    def __eq__(self, other):
        if not isinstance(other, TraceItem):
            return False
        else:
            return super(TraceItem, self).__eq__(other)

    def __hash__(self):
        return hash((TraceItem, self._attributes))

    @classmethod
    def deserialize_attribute(cls, key, value):
        if key == 'tree':
            return AbstractNode.deserialize_attribute(key, value)
        else:
            return value
