from .abstractnode import AbstractNode
from .triple import Triple

__all__ = ['AbstractNode', 'Triple', 'type_to_class']

type_to_class = {
        'triple': Triple
        }
