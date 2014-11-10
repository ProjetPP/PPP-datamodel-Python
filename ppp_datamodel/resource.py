"""Contains the class representing a resource leaf."""

import logging
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
