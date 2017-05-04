import sys
import json

from .traceitem import TraceItem
from ..nodes import AbstractNode
from .traceitem import TraceItem
from ..exceptions import AttributeNotProvided
from ..utils import SerializableAttributesHolder

if sys.version_info[0] >= 3:
    basestring = str

class Request(SerializableAttributesHolder):
    """Represents a request.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#request
    """
    __slots__ = ()
    _possible_attributes = ('id', 'language', 'tree', 'measures', 'trace', 'response_language')

    def _check_attributes(self, attributes, extra=None):
        super(Request, self)._check_attributes(attributes)
        missing_attributes = {'id', 'language', 'tree'} - set(attributes.keys())
        if missing_attributes:
            raise AttributeNotProvided('Missing attributes: %s' % ', '.join(missing_attributes))
        if not isinstance(attributes['language'], basestring):
            raise TypeError('"language" attribute is not a string.')
        attributes.setdefault('measures', {})
        attributes.setdefault('trace', [])
        if 'response_language' not in attributes:
            attributes['response_language'] = attributes['language']
        elif not isinstance(attributes['response_language'], basestring):
            raise TypeError('"response_language" attribute is not a string.')
        if not isinstance(attributes['tree'], AbstractNode):
            raise TypeError('"tree" attribute is not an AbstractNode.')
        if not isinstance(attributes['measures'], dict):
            raise TypeError('"measures" attribute is not a dict.')
        if not isinstance(attributes['trace'], list):
            raise TypeError('"trace" attribute is not a list.')

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
