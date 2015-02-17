"""Contains the base class for PPP nodes."""

import json

from ..log import logger
from .. import exceptions

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

        self._parse_attributes(attributes)
        self._attributes['type'] = self.type

    def _check_attributes(self, attributes, extra=None):
        """Check if attributes given to the constructor can be used to
        instanciate a valid node."""
        extra = extra or ()
        if 'type' in attributes:
            assert attributes.pop('type') == self.type
        unknown_keys = set(attributes) - set(self._possible_attributes) - set(extra)
        if unknown_keys:
            logger.warning('%s node got unknown attributes: %s' %
                            (self._type, unknown_keys))

    def _parse_attributes(self, attributes):
        self._attributes = attributes

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

    def __hash__(self):
        return hash(frozenset(self._attributes.items()))

    def fold(self, predicate):
        """Takes a predicate and applies it to each node starting from the
        leaves and making the return value propagate."""
        childs = {x:y.fold(predicate) for (x,y) in self._attributes.items()
                  if isinstance(y, AbstractNode)}
        return predicate(self, childs)

    def get(self, name, strict=True):
        """Get an attribute of the node (read-only access)."""
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
            super().__setattr__(name, value)
        else:
            raise TypeError('%s\'s attributes are not settable.' %
                    self.__class__.__name__)
    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name, value)
        else:
            raise TypeError('%s\'s attributes are not settable.' %
                    self.__class__.__name__)

    def has(self, name):
        """Check existence of an attribute."""
        return name in self._attributes
    __hasattr__ = __contains__ = has

    def as_dict(self):
        """Returns a JSON-serializeable object representing this tree."""
        conv = lambda v: v.as_dict() if isinstance(v, AbstractNode) else v
        return {k.replace('_', '-'): conv(v) for (k, v) in self._attributes.items()}
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
        assert isinstance(data, str)
        data = json.loads(data)
        assert isinstance(data, dict)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data):
        cls._test_can_import_json(data)

        # Find a class that will deserialize the dict as specifically
        # as possible
        while True:
            cls2 = cls._select_class(data)
            if cls is cls2:
                break
            cls = cls2
        conv = (lambda k,v: cls.deserialize_attribute(k, v)
                            if isinstance(v, dict) else v)
        data = {k.replace('-', '_'): conv(k,v) for (k, v) in data.items()}
        return cls(**data)

    @classmethod
    def deserialize_attribute(cls, key, value):
        return AbstractNode.from_dict(value)

    @classmethod
    def _select_class(cls, data):
        return TYPE_TO_CLASS[data['type']]

    def traverse(self, predicate):
        def wrapper(tree):
            if isinstance(tree, AbstractNode):
                return tree.traverse(predicate)
            else:
                return tree
        arguments = {x: wrapper(y)
                     for (x, y) in self._attributes.items()
                     if x != 'type'}
        return predicate(self.__class__(**arguments))
