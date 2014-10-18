"""Utilities for using the PPP datamodel."""

from . import Missing

def contains_missing(tree):
    def predicate(node, childs):
        if isinstance(node, Missing):
            return True
        else:
            return any(childs.values())
    return tree.fold(predicate)
