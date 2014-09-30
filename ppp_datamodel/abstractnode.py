import json

from . import exceptions

class AbstractNode:
    """Base class for PPP nodes."""
    __slots__ = ('_attributes')
    _type = None
    _possible_attributes = None
    def __init__(self, **attributes):
        # Sanity checks
        if self._type is None or self._possible_attributes is None:
            raise TypeError('%s is an abstract class.' % self.__class__)
        if 'type' in attributes:
            assert attributes.pop('type') == self.type
        unknown_keys = set(attributes) - set(self._possible_attributes)
        if unknown_keys:
            raise TypeError('%s node got unknown attributes: %s' %
                    (self._type, unknown_keys))

        # Add the attributes object
        self._attributes = attributes
        self._attributes['type'] = self.type

    @property
    def type(self):
        return self._type

    def __repr__(self):
        return '<PPP node "%s" %r>' % (self.type, self._attributes)

    # Get an attribute (read-only)
    def get(self, name):
        if name not in self._possible_attributes:
            raise AttributeError('%s is not a valid attribute of %r.' %
                    (name, self))
        elif name in self._attributes:
            return self._attributes[name]
        else:
            raise exceptions.AttributeNotProvided(name)
    __getattr__ = __getitem__ = get

    # Check presence of an attribute
    def has(self, name):
        return name in self._attributes
    __hasattr__ = __contains__ = has

    # Get a JSON dump of the object
    def as_json(self):
        conv = lambda v:v.as_json() if isinstance(v, AbstractNode) else v
        return json.dumps({k: conv(v) for (k, v) in self._attributes.items()})

    @classmethod
    def from_json(cls, data):
        # Decode JSON string
        if isinstance(data, str):
            data = json.loads(data)
        assert isinstance(data, dict)

        from . import type_to_class

        # Sanity checks
        if 'type' not in data:
            raise exceptions.AttributeNotProvided('type')
        if data['type'] not in type_to_class:
            raise exceptions.UnknownNodeType(data['type'])

        # Create node instances
        conv = lambda v:cls.from_json(v) if isinstance(v, dict) else v
        data = {k: conv(v) for (k, v) in data.items()}
        return type_to_class[data['type']](**data)

