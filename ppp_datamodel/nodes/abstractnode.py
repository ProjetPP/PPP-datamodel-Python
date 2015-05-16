"""Contains the base class for PPP nodes."""

from ..utils.typedattributesholder import TypedAttributesHolder
from ..utils.serializableattributesholder import SerializableAttributesHolder
from ..log import logger
from .. import exceptions

class SerializableTypedAttributesHolder(SerializableAttributesHolder, TypedAttributesHolder):

    @staticmethod
    def _test_can_import_json(data):
        """Sanity check on input JSON data"""
        if 'type' not in data:
            raise exceptions.AttributeNotProvided('type')
        if data['type'] not in TYPE_TO_CLASS:
            raise exceptions.UnknownNodeType(data['type'])

    @classmethod
    def _select_class(cls, data):
        return TYPE_TO_CLASS[data['type']]

    def __eq__(self, other):
        if isinstance(other, dict):
            return self == SerializableTypedAttributesHolder.from_dict(other)
        else:
            return super(SerializableTypedAttributesHolder, self).__eq__(other)

    def __hash__(self):
        return super(SerializableTypedAttributesHolder, self).__hash__()

TYPE_TO_CLASS = {}
def register(cls):
    """Register a class to make it available to the deserializer."""
    assert cls._type
    TYPE_TO_CLASS[cls._type] = cls
    return cls

class AbstractNode(SerializableTypedAttributesHolder):
    """SerializableAttributesHolder with methods for making operations
    on trees."""
    def fold(self, predicate):
        """Takes a predicate and applies it to each node starting from the
        leaves and making the return value propagate."""
        childs = {x:y.fold(predicate) for (x,y) in self._attributes.items()
                  if isinstance(y, SerializableTypedAttributesHolder)}
        return predicate(self, childs)

    def traverse(self, predicate):
        def wrapper(tree):
            if isinstance(tree, SerializableTypedAttributesHolder):
                return tree.traverse(predicate)
            else:
                return tree
        arguments = {x: wrapper(y)
                     for (x, y) in self._attributes.items()
                     if x != 'type'}
        return predicate(self.__class__(**arguments))
