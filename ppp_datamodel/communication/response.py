import sys
import json

from ..nodes import AbstractNode
from .traceitem import TraceItem
from ..exceptions import AttributeNotProvided
from ..utils import SerializableAttributesHolder

if sys.version_info[0] >= 3:
    basestring = str

class Response(SerializableAttributesHolder):
    """Represents a response.
    https://github.com/ProjetPP/Documentation/blob/master/module-communication.md#response
    """
    __slots__ = ()
    _possible_attributes = ('language', 'tree', 'measures', 'trace')


    def _check_attributes(self, attributes, extra=None):
        super(Response, self)._check_attributes(attributes)
        missing_attributes = {'language', 'tree', 'measures', 'trace'} - set(attributes.keys())
        if missing_attributes:
            raise AttributeNotProvided('Missing attributes: %s' % ', '.join(missing_attributes))
        if not isinstance(attributes['language'], basestring):
            raise TypeError('"language" attribute is not a string.')
        if not isinstance(attributes['tree'], AbstractNode):
            raise TypeError('"tree" attribute is not an AbstractNode.')
        if not isinstance(attributes['measures'], dict):
            raise TypeError('"measures" attribute is not a dict.')
        if not isinstance(attributes['trace'], list):
            raise TypeError('"trace" attribute is not a list.')

    def _parse_attributes(self, attributes):
        tree = attributes['tree']
        if isinstance(tree, dict):
            tree = AbstractNode.from_dict(tree)
        elif isinstance(tree, str):
            tree = AbstractNode.from_json(tree)
        attributes['tree'] = tree
        attributes['trace'] = \
                [x if isinstance(x, TraceItem) else TraceItem.from_dict(x)
                 for x in attributes['trace']]
        super(Response, self)._parse_attributes(attributes)

    def __eq__(self, other):
        if not isinstance(other, Response):
            return False
        else:
            return super(Response, self).__eq__(other)

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
