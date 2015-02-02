"""Utilities for using the PPP datamodel."""

from . import Resource, Triple, Missing, Intersection, List, Union, And, Or, Exists, First, Last, Sort

def contains_missing(tree):
    def predicate(node, childs):
        if isinstance(node, Missing):
            return True
        else:
            return any(childs.values())
    return tree.fold(predicate)

def isincluded(tree1, tree2):
    """
        Return True if and only if tree1 is included in tree2.
    """
    if isinstance(tree1,Resource):
        tree1=List([tree1])
    if isinstance(tree2,Resource):
        tree2=List([tree2])
    if type(tree1) != type(tree2):
        return False
    elif isinstance(tree1, Missing):
        return True
    elif isinstance(tree1, List):
        return set(tree1.list).issubset(set(tree2.list))
    elif isinstance(tree1, triple):
        return  isincluded(tree1.subject, tree2.subject) and\
            isincluded(tree1.predicate, tree2.predicate) and\
            isincluded(tree1.object, tree2.object)
    elif isinstance(tree1,Sort):
        return tree1.predicate == tree2.predicate and isincluded(tree1.list, tree2.list)
    elif isinstance(tree1,(First, Last, Exists)):
        return isincluded(tree1.list, tree2.list)
    elif isinstance(tree1,(Intersection, Union, And, Or)):
        if len(tree1.list) != len(tree2.list):
            return False
        for elt in tree1.list:
            if not any(isincluded(elt,x) for x in tree2.list):
                return False
        return True
    else:
        raise Exception('Unknown class.')
