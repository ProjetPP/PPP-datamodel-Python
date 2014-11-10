"""Contains the class representing a resource leaf."""

import logging
import dateutil.parser
from .abstractnode import register, AbstractNode

EXTRA_ATTRIBUTES = {
        'string': ('language',),
        'boolean': (),
        'time': ('calendar',),
        }

@register
class Resource(AbstractNode):
    """Represents a resource.
    https://github.com/ProjetPP/Documentation/blob/master/data-model.md#resource
    """
    __slots__ = ()
    _type = 'resource'
    _possible_attributes = ('value', 'value_type')

    def _check_attributes(self, attributes):
        type_ = attributes.get('value_type', 'string')
        if type_ not in EXTRA_ATTRIBUTES:
            logging.warning('Unknown value-type: %s' % type_)
        extra = EXTRA_ATTRIBUTES.get(type_, ())
        super()._check_attributes(attributes,
                                  extra=extra)

    def _parse_attributes(self, attributes):
        type_ = attributes.get('value_type', 'string')
        value = attributes.get('value', None)
        if type_ == 'boolean':
            value = self._parse_boolean(value, attributes)
        elif type_ == 'time':
            value = self._parse_time(value, attributes)
        attributes['value'] = value
        self._attributes = attributes

    @staticmethod
    def _parse_boolean(value, attributes):
        if value in ('1', 'true'):
            return True
        elif value in ('0', 'false'):
            return False
        else:
            raise ValueError('Could not parse value %r of value-type %s'%
                             (value, type_))

    @staticmethod
    def _parse_time(value, attributes):
        calendar = attributes.get('calendar', 'gregorian')
        if calendar not in ('gregorian',):
            logging.warning('Unknown calendar %r. Parsing as gregorian.'%
                            calendar)
        return dateutil.parser.parse(value)
