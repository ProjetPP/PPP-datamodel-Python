"""Contains the base class for PPP nodes."""

import json

from . import exceptions

TYPE_TO_CLASS = {}
def register(cls):
    """Register a class to make it available to the deserializer."""
    assert cls._type
    TYPE_TO_CLASS[cls._type] = cls
    return cls

class AbstractNode:
    """Base class for PPP nodes."""
    __slots__ = ('_attributes')
    _type = None
    _possible_attributes = None
    def __init__(self, *args, **attributes):
        # Sanity checks
        if self._type is None or self._possible_attributes is None:
            raise TypeError('%s is an abstract class.' % self.__class__)
        attributes.update(dict(zip(self._possible_attributes, args)))
        self._check_attributes(attributes)

        # Add the attributes object
        self._attributes = attributes
        self._attributes['type'] = self.type

    def _check_attributes(self, attributes):
        """Check if attributes given to the constructor can be used to
        instanciate a valid node."""
        if 'type' in attributes:
            assert attributes.pop('type') == self.type
        unknown_keys = set(attributes) - set(self._possible_attributes)
        if unknown_keys:
            raise TypeError('%s node got unknown attributes: %s' %
                            (self._type, unknown_keys))

    @property
    def type(self):
        """Type of the node."""
        return self._type

    def __repr__(self):
        return '<PPP node "%s" %r>' % (self.type,
                {x:y for (x,y) in self._attributes.items() if x != 'type'})

    def __eq__(self, other):
        """Tests equality with another abstractnode instance."""
        if isinstance(other, dict):
            return self.as_dict() == other
        elif isinstance(other, AbstractNode):
            return self._attributes == other._attributes
        else:
            return False

    def fold(self, predicate):
        """Takes a predicate and applies it to each node starting from the
        leaves and making the return value propagate."""
        childs = {x:y.fold(predicate) for (x,y) in self._attributes.items()
                  if isinstance(y, AbstractNode)}
        return predicate(self, childs)

    def get(self, name):
        """Get an attribute of the node (read-only access)."""
        if name not in self._possible_attributes:
            raise AttributeError('%s is not a valid attribute of %r.' %
                                 (name, self))
        elif name in self._attributes:
            return self._attributes[name]
        else:
            raise exceptions.AttributeNotProvided(name)
    __getattr__ = __getitem__ = get

    def has(self, name):
        """Check existence of an attribute."""
        return name in self._attributes
    __hasattr__ = __contains__ = has

    def as_dict(self):
        """Returns a JSON-serializeable object representing this tree."""
        conv = lambda v: v.as_dict() if isinstance(v, AbstractNode) else v
        return {k: conv(v) for (k, v) in self._attributes.items()}
    def as_json(self):
        """Return a JSON dump of the object."""
        return json.dumps(self.as_dict())

    @staticmethod
    def _test_can_import_json(data):
        """Sanity check on input JSON data"""
        if 'type' not in data:
            raise exceptions.AttributeNotProvided('type')
        if data['type'] not in TYPE_TO_CLASS:
            raise exceptions.UnknownNodeType(data['type'])

    @classmethod
    def from_json(cls, data):
        """Decode a JSON string and inflate a node instance."""
        # Decode JSON string
        if isinstance(data, str):
            data = json.loads(data)
        assert isinstance(data, dict)

        cls._test_can_import_json(data)

        # Create node instances
        conv = lambda v: cls.from_json(v) if isinstance(v, dict) else v
        data = {k: conv(v) for (k, v) in data.items()}
        return TYPE_TO_CLASS[data['type']](**data)

