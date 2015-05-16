from .attributesholder import AttributesHolder

class TypedAttributesHolder(AttributesHolder):
    """AttributesHolder with a special attributes holding type."""
    __slots__ = ()
    _type = None
    def __init__(self, *args, **attributes):
        # Sanity checks
        if self._type is None or self._possible_attributes is None:
            raise TypeError('%s is an abstract class.' % self.__class__)
        super(TypedAttributesHolder, self).__init__(*args, **attributes)

        self._attributes['type'] = self.type

    def _check_attributes(self, attributes, extra=None):
        if 'type' in attributes:
            assert attributes.pop('type') == self.type
        return super(TypedAttributesHolder, self) \
                ._check_attributes(attributes, extra)

    @property
    def type(self):
        """Type of the node."""
        return self._type

    def __repr__(self):
        return '<PPP node "%s" %r>' % (self.type,
                {x:y for (x,y) in self._attributes.items() if x != 'type'})

    def __eq__(self, other):
        """Tests equality with another AttributesHolder instance."""
        if isinstance(other, dict):
            return self.as_dict() == other
        elif isinstance(other, TypedAttributesHolder) and \
                self._type == other._type:
            return super(TypedAttributesHolder, self).__eq__(other)
        else:
            return NotImplemented

    def __hash__(self):
        return hash(frozenset(self._attributes.items()))

