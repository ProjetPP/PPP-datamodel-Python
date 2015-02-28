"""Contains the base class for PPP nodes."""

import json

from ..utils.typedattributesholder import TypedAttributesHolder
from ..log import logger
from .. import exceptions

TYPE_TO_CLASS = {}
def register(cls):
    """Register a class to make it available to the deserializer."""
    assert cls._type
    TYPE_TO_CLASS[cls._type] = cls
    return cls

class SerializableAttributesHolder(TypedAttributesHolder):
    """TypedAttributesHolder with methods handling serialization and
    deserialization according to the PPP datamodel specification."""
    def as_dict(self):
        """Returns a JSON-serializeable object representing this tree."""
        def conv(v):
            if isinstance(v, SerializableAttributesHolder):
                return v.as_dict()
            else:
                return v
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
        return cls.from_dict(value)

    @classmethod
    def _select_class(cls, data):
        return TYPE_TO_CLASS[data['type']]

class AbstractNode(SerializableAttributesHolder):
    """SerializableAttributesHolder with methods for making operations
    on trees."""
    def fold(self, predicate):
        """Takes a predicate and applies it to each node starting from the
        leaves and making the return value propagate."""
        childs = {x:y.fold(predicate) for (x,y) in self._attributes.items()
                  if isinstance(y, TypedAttributesHolder)}
        return predicate(self, childs)

    def traverse(self, predicate):
        def wrapper(tree):
            if isinstance(tree, TypedAttributesHolder):
                return tree.traverse(predicate)
            else:
                return tree
        arguments = {x: wrapper(y)
                     for (x, y) in self._attributes.items()
                     if x != 'type'}
        return predicate(self.__class__(**arguments))
