"""Contains the class representing a resource leaf."""

from .log import logger
from .abstractnode import register, AbstractNode

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
        type_ = data.get('value_type', 'string')
        if type_ not in VALUE_TYPE_TO_CLASS:
            logger.warning('Unknown value-type: %s' % type_)
            type_ = 'string'
        return VALUE_TYPE_TO_CLASS[type_]

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
        type_ = d.get('value-type', 'string')
        value = d.get('value')
        d['value'] = self._format_value(value)
        return d

@register_valuetype
class StringResource(Resource):
    _value_type = 'string'
    _possible_attributes = Resource._possible_attributes + ('language',)

@register_valuetype
class MathLatexResource(Resource):
    _value_type = 'math-latex'

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

