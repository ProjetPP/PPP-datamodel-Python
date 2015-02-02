"""Utilities for using the PPP datamodel."""

from . import Resource, Triple, Missing, Intersection, List, Union, And, Or, Exists, First, Last, Sort
import unittest

def contains_missing(tree):
    def predicate(node, childs):
        if isinstance(node, Missing):
            return True
        else:
            return any(childs.values())
    return tree.fold(predicate)

class InclusionAssertion:

    def isincluded(self,tree1, tree2, originalTree1, originalTree2):
        """
            Check wether tree1 is included in tree2.
            originalTree1 and originalTree2 are the trees given at the call of assertIncluded.
        """
        if isinstance(tree1,Resource):
            tree1=List([tree1])
        if isinstance(tree2,Resource):
            tree2=List([tree2])
        if type(tree1) != type(tree2):
            raise AssertionError('Different types for %s and %s.\n%s ⊈ %s.' % (tree1, tree2, originalTree1, originalTree2))
        elif isinstance(tree1, Missing):
            return
        elif isinstance(tree1, List):
            if not set(tree1.list).issubset(set(tree2.list)):
                raise AssertionError('List %s not included in List %s.\n%s ⊈ %s.' % (tree1, tree2, originalTree1, originalTree2))
        elif isinstance(tree1, Triple):
            return  self.isincluded(tree1.subject, tree2.subject, originalTree1, originalTree2) and\
                self.isincluded(tree1.predicate, tree2.predicate, originalTree1, originalTree2) and\
                self.isincluded(tree1.object, tree2.object)
        elif isinstance(tree1,Sort):
            if tree1.predicate != tree2.predicate:
                raise AssertionError('Different predicate: %s and %s.\n%s ⊈ %s.' % (tree1.predicate, tree2.predicate, originalTree1, originalTree2))
            else:
                return self.isincluded(tree1.list, tree2.list, originalTree1, originalTree2)
        elif isinstance(tree1,(First, Last, Exists)):
            return self.isincluded(tree1.list, tree2.list, originalTree1, originalTree2)
        elif isinstance(tree1,(Intersection, Union, And, Or)):
            if len(tree1.list) != len(tree2.list):
                raise AssertionError('Different list length for %s and %s.\n%s ⊈ %s.' % (tree1, tree2, originalTree1, originalTree2))
            for elt in tree1.list:
                if not self.contains(elt,tree2.list):
                    raise AssertionError('%s does not belong to %s.\n%s ⊈ %s.' % (elt, tree2.list, originalTree1, originalTree2))
            return
        else:
            raise Exception('Unknown class.')

    def contains(self,elt,l):
        """
            Return True if and only if l contains elt (in the isincluded meaning).
        """
        included = False
        for elt2 in l:
            try:
                self.isincluded(elt,elt2,None,None)
            except AssertionError:
                continue
            included = True
            break
        return included

    def assertIncluded(self,tree1,tree2):
        """
            Check wether tree1 is included in tree2.
        """
        return self.isincluded(tree1,tree2,tree1,tree2)
