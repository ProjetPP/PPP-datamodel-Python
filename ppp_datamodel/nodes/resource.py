"""Contains the class representing a resource leaf."""

from ..log import logger
from .abstractnode import register, AbstractNode

__all__ = ['Resource', 'StringResource', 'MathLatexResource',
           'BooleanResource', 'TimeResource',
           'JsonldResource']

EXTRA_ATTRIBUTES = {
        'string': ('language',),
        'boolean': (),
        'time': ('calendar',),
        }

VALUE_TYPE_TO_CLASS = {}
def register_valuetype(cls):
    VALUE_TYPE_TO_CLASS[cls._value_type] = cls
    return cls


@register
@register_valuetype
class Resource(AbstractNode):
    """Represents a resource.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#resource
    """
    __slots__ = ()
    _type = 'resource'
    _value_type = 'unknown'
    _possible_attributes = ('value', 'value_type')

    @classmethod
    def _select_class(cls, data):
        type_ = data.get('value-type', 'string')
        if type_ not in VALUE_TYPE_TO_CLASS:
            logger.warning('Unknown value-type: %s' % type_)
            type_ = 'string'
        return VALUE_TYPE_TO_CLASS[type_]

    def _check_attributes(self, attributes):
        super()._check_attributes(attributes)
        if not isinstance(attributes['value'], str):
            raise TypeError('%s\'s value must be a string, not %r.' %
                    attributes['value'])

    def _parse_attributes(self, attributes):
        attributes['value'] = self._parse_value(attributes.get('value', None),
                                                attributes)
        super()._parse_attributes(attributes)

    @staticmethod
    def _parse_value(value, attributes):
        return value

    @staticmethod
    def _format_value(value):
        return value

    def as_dict(self):
        d = super().as_dict()
        type_ = d.get('value-type', self._value_type)
        value = d.get('value')
        d['value'] = self._format_value(value)
        if type_ not in ('string', 'unknown') or 'value-type' in d:
            d['value-type'] = type_
        return d

@register_valuetype
class StringResource(Resource):
    _value_type = 'string'
    _possible_attributes = Resource._possible_attributes + ('language',)

@register_valuetype
class MathLatexResource(Resource):
    _value_type = 'math-latex'
    _possible_attributes = Resource._possible_attributes + ('latex',)

@register_valuetype
class BooleanResource(Resource):
    _value_type = 'boolean'

    @staticmethod
    def _parse_value(value, attributes):
        if value in ('1', 'true'):
            return True
        elif value in ('0', 'false'):
            return False
        else:
            raise ValueError('Could not parse value %r of value-type %s'%
                             (value, type_))
    @staticmethod
    def _format_value(value):
        return 'true' if value else 'false'

@register_valuetype
class TimeResource(Resource):
    _value_type = 'time'
    _possible_attributes = Resource._possible_attributes + ('calendar',)

    @staticmethod
    def _parse_value(value, attributes):
        return value

    @staticmethod
    def _format_value(value):
        return value

def freeze_dicts(d):
    if isinstance(d, dict):
        return frozenset(map(lambda x:(x[0], freeze_dicts(x[1])), d.items()))
    elif isinstance(d, list):
        return tuple(map(freeze_dicts, d))
    else:
        return d

@register_valuetype
class JsonldResource(Resource):
    _value_type = 'resource-jsonld'
    _possible_attributes = Resource._possible_attributes + ('graph',)

    @classmethod
    def deserialize_attribute(cls, key, value):
        if key == 'graph':
            return value
        else:
            super().deserialize_attribute(key, value)

    def __hash__(self):
        raise TypeError('%s instances are not hashable.' % self.__class__)

    def get_uris(self):
        uris = set()
        if '@id' in self.graph:
            uris.add(self.graph['@id'])
        same_as = self.graph.get('sameAs', [])
        if isinstance(same_as, str):
            same_as = [same_as]
        assert isinstance(same_as, list)
        uris.update(same_as)
        return uris

    def __eq__(self, other):
        if not isinstance(other, JsonldResource):
            return False
        return self.graph == other.graph or \
                bool(self.get_uris() & other.get_uris())
