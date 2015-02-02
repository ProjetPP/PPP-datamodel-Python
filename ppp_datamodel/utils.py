"""Utilities for using the PPP datamodel."""

from . import Resource, Triple, Missing, Intersection, List, Union, And, Or, Exists, First, Last, Sort

def contains_missing(tree):
    def predicate(node, childs):
        if isinstance(node, Missing):
            return True
        else:
            return any(childs.values())
    return tree.fold(predicate)

def isincluded(tree1,tree2):
    """
        Return True if and only if tree1 is included in tree2.
    """
    if isinstance(tree1,Resource):
        tree1=List([tree1])
    if isinstance(tree2,Resource):
        tree2=List([tree2])
    if type(tree1) != type(tree2):
        return False
    if isinstance(tree1,Missing):
        return True
    if isinstance(tree1,List):
        return set(tree1.list).issubset(set(tree2.list))
    if isinstance(tree1,Triple):
        return  isincluded(tree1.subject,tree2.subject) and\
            isincluded(tree1.predicate,tree2.predicate) and\
            isincluded(tree1.object,tree2.object)
    if isinstance(tree1,Sort):
        return tree1.predicate == tree2.predicate and isincluded(tree1.list,tree2.list)
    return isincluded(tree1.list,tree2.list)
