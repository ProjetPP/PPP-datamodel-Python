"""Module containing exception classes."""

class PPPDatamodelException(Exception):
    """Base class for PPP exceptions."""
    pass
class AttributeNotProvided(PPPDatamodelException):
    """Exception raised when a mandatory attribute is not given to
    a node constructor."""
    pass
class UnknownNodeType(PPPDatamodelException):
    """Exception raised when a node type has no constructor/class."""
    pass
