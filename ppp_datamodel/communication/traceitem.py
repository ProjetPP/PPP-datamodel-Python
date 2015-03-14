import json

from ..nodes import AbstractNode
from ..utils import SerializableAttributesHolder

class TraceItem(SerializableAttributesHolder):
    """Represents a trace item.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#format-of-a-trace-item
    """
    __slots__ = ()
    _possible_attributes = ('module', 'tree', 'measures')

    def _check_attributes(self, attributes, extra=None):
        super(TraceItem, self)._check_attributes(attributes)
        assert {'module', 'tree', 'measures'} == \
                set(attributes.keys()), (attributes, extra)

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
