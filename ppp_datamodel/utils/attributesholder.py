from .. import exceptions
from ..log import logger

class AttributesHolder(object):
    """Stores attributes and provides read-only access to them."""
    __slots__ = ('_attributes')
    _possible_attributes = None
    def __init__(self, *args, **attributes):
        attributes.update(dict(zip(self._possible_attributes, args)))
        self._check_attributes(attributes)
        self._parse_attributes(attributes)

    def _check_attributes(self, attributes, extra=None):
        """Check if attributes given to the constructor can be used to
        instanciate a valid node."""
        extra = extra or ()
        unknown_keys = set(attributes) - set(self._possible_attributes) - set(extra)
        if unknown_keys:
            logger.warning('%s got unknown attributes: %s' %
                            (self.__class__.__name__, unknown_keys))

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__,
                {x:y for (x,y) in self._attributes.items()})

    def _parse_attributes(self, attributes):
        self._attributes = attributes

    def __eq__(self, other):
        """Tests equality with another AttributesHolder instance."""
        if isinstance(other, AttributesHolder):
            return self._attributes == other._attributes
        else:
            return False
    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(frozenset(self._attributes.items()))

    def get(self, name, strict=True):
        """Get an attribute of the holder (read-only access)."""
        if not isinstance(name, str) or name.startswith('_'):
            raise AttributeError(self.__class__.__name__, name)
        elif strict and name not in self._possible_attributes:
            raise AttributeError('%s is not a valid attribute of %r.' %
                                 (name, self))
        elif name in self._attributes:
            return self._attributes[name]
        else:
            raise exceptions.AttributeNotProvided(name)
    __getattr__ = __getitem__ = get

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super(AttributesHolder, self).__setattr__(name, value)
        else:
            raise TypeError('%s\'s attributes are not settable.' %
                    self.__class__.__name__)
    def __delattr__(self, name):
        if name.startswith('_'):
            super(AttributesHolder, self).__delattr__(name, value)
        else:
            raise TypeError('%s\'s attributes are not settable.' %
                    self.__class__.__name__)

    def has(self, name):
        """Check existence of an attribute."""
        return name in self._attributes
    __hasattr__ = __contains__ = has

