import sys
import json

from ..nodes import AbstractNode
from ..exceptions import AttributeNotProvided
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
        missing_attributes = {'module', 'tree', 'measures'} - set(attributes.keys())
        if missing_attributes:
            raise AttributeNotProvided('Missing attributes: %s' % ', '.join(missing_attributes))
        if not isinstance(attributes['module'], basestring):
            raise TypeError('"module" attribute is not a string.')
        if not isinstance(attributes['tree'], AbstractNode):
            raise TypeError('"tree" attribute is not an AbstractNode.')
        if not isinstance(attributes['measures'], dict):
            raise TypeError('"measures" attribute is not a dict.')
        if 'times' in attributes and not isinstance(attributes['times'], dict):
            raise TypeError('"times" attribute is not a dict.')

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
