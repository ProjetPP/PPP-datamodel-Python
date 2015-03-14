import json

from .attributesholder import AttributesHolder

class SerializableAttributesHolder(AttributesHolder):
    """AttributesHolder with methods handling serialization and
    deserialization according to the PPP datamodel specification."""
    def as_dict(self):
        """Returns a JSON-serializeable object representing this tree."""
        def conv(v):
            if isinstance(v, SerializableAttributesHolder):
                return v.as_dict()
            elif isinstance(v, list):
                return [conv(x) for x in v]
            elif isinstance(v, dict):
                return {x:conv(y) for (x,y) in v.items()}
            else:
                return v
        return {k.replace('_', '-'): conv(v) for (k, v) in self._attributes.items()}
    def as_json(self):
        """Return a JSON dump of the object."""
        return json.dumps(self.as_dict())

    @staticmethod
    def _test_can_import_json(data):
        """Sanity check on input JSON data"""
        pass

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
        return cls
