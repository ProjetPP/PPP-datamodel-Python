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

class InclusionTestCase(unittest.TestCase):
    """
    Unit test with a method for asserting inclusion of objects from the
    datamodel.
    """
    def assertIncluded(self, tree1, tree2,
                       originalTree1=None, originalTree2=None):
        """
        Check wether tree1 is included in tree2.
        originalTree1 and originalTree2 are the whole trees we run the
        assertion on.
        """
        originalTree1 = originalTree1 or tree1
        originalTree2 = originalTree2 or tree2
        if isinstance(tree1, Resource):
            tree1=List([tree1])
        if isinstance(tree2, Resource):
            tree2=List([tree2])
        if type(tree1) != type(tree2):
            raise AssertionError('Different types for %s and %s.\n%s ⊈ %s.' %
                    (tree1, tree2, originalTree1, originalTree2))
        elif isinstance(tree1, Missing):
            return
        elif isinstance(tree1, List):
            if not set(tree1.list).issubset(set(tree2.list)):
                raise AssertionError(
                        'List %s not included in List %s.\n%s ⊈ %s.' %
                        (tree1, tree2, originalTree1, originalTree2))
        elif isinstance(tree1, Triple):
            self.assertIncluded(tree1.subject, tree2.subject,
                    originalTree1, originalTree2)
            self.assertIncluded(tree1.predicate, tree2.predicate,
                        originalTree1, originalTree2)
            self.assertIncluded(tree1.object, tree2.object)
        elif isinstance(tree1, Sort):
            if tree1.predicate != tree2.predicate:
                raise AssertionError(
                        'Different predicate: %s and %s.\n%s ⊈ %s.' %
                        (tree1.predicate, tree2.predicate,
                            originalTree1, originalTree2))
            else:
                self.assertIncluded(tree1.list, tree2.list,
                        originalTree1, originalTree2)
        elif isinstance(tree1, (First, Last, Exists)):
            self.assertIncluded(tree1.list, tree2.list,
                    originalTree1, originalTree2)
        elif isinstance(tree1, (Intersection, Union, And, Or)):
            if len(tree1.list) != len(tree2.list):
                raise AssertionError(
                        'Different list length for %s and %s.\n%s ⊈ %s.' %
                        (tree1, tree2, originalTree1, originalTree2))
            for elt in tree1.list:
                if not self.contains(elt, tree2.list):
                    raise AssertionError(
                            '%s does not belong to %s.\n%s ⊈ %s.' %
                            (elt, tree2.list, originalTree1, originalTree2))
            return
        else:
            raise TypeError('Object of unknown class: %r' % (tree1,))

    def contains(self, elt, l):
        """
        Return True if and only if l contains elt (in the isincluded meaning).
        """
        for elt2 in l:
            try:
                self.assertIncluded(elt, elt2, None, None)
            except AssertionError:
                continue
            return True
        return False
