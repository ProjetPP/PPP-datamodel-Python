from unittest import TestCase
import itertools

from ppp_datamodel import Resource, Triple, Missing, Intersection, Union, List, Union, And, Or, Exists, First, Last, Sort
from ppp_datamodel import utils

T = Triple
R = Resource
M = Missing

class UtilsTests(utils.InclusionTestCase):
    def testContainsMissing(self):
        f = utils.contains_missing
        self.assertTrue(f(T(subject=R(value='foo'), object=T(subject=M()))))
        self.assertFalse(f(T(subject=R(value='foo'), object=T(subject=R()))))
        self.assertTrue(f(M()))
    def testInclusionBasic(self):
        self.assertIncluded(Missing(), Missing())
        self.assertIncluded(Resource('foo'), Resource('foo'))
        with self.assertRaises(AssertionError):
            self.assertIncluded(Resource('foo'), Resource('bar'))
        self.assertIncluded(List([Resource('foo')]), Resource('foo'))
        with self.assertRaises(AssertionError):
            self.assertIncluded(List([Resource('foo')]), Resource('bar'))
        self.assertIncluded(Resource('foo'), List([Resource('foo')]))
        with self.assertRaises(AssertionError):
            self.assertIncluded(Resource('foo'), List([Resource('bar')]))
        self.assertIncluded(List([Resource('foo')]), List([Resource('foo')]))
        with self.assertRaises(AssertionError):
            self.assertIncluded(List([Resource('foo')]),
                    List([Resource('bar')]))
        self.assertIncluded(List([Resource('foo')]),
                List([Resource('foo'), Resource('bar')]))
        with self.assertRaises(AssertionError):
            self.assertIncluded(List([Resource('foo'), Resource('bar')]),
                    List([Resource('foo')]))
    def testInclusionDifferentType(self):
        l = [Resource('foo'), Missing(), Triple(Resource('foo'),
            Resource('foo'), Resource('foo')),\
            Intersection([Resource('foo')]), Union([Resource('foo')]),\
            And([Resource('foo')]), Or([Resource('foo')]),
            Exists(Resource('foo')), First(Resource('foo')),
            Last(Resource('foo')), Sort(Resource('foo'), Resource('pred'))]
        for (t1, t2) in itertools.permutations(l, 2):
            with self.assertRaises(AssertionError):
                self.assertFalse(self.assertIncluded(t1, t2))
    def testInclusionTriple(self):
        tree1=Triple(Resource('foo'),
                List([Resource('a'), Resource('b')]), Missing())
        tree2=Triple(List([Resource('bar'), Resource('foo')]),
                List([Resource('a'), Resource('d'), Resource('b')]), Missing())
        self.assertIncluded(tree1, tree2)
        with self.assertRaises(AssertionError):
            self.assertIncluded(tree2, tree1)
    def testInclusionFirstLastSort(self):
        tree1=Triple(Resource('foo'), List([Resource('a'), Resource('b')]),
                Missing())
        tree2=Triple(List([Resource('bar'), Resource('foo')]),
                List([Resource('a'), Resource('d'), Resource('b')]), Missing())
        for op in [Last,First]:
            self.assertIncluded(op(tree1), op(tree2))
            with self.assertRaises(AssertionError):
                self.assertIncluded(op(tree2), op(tree1))
        self.assertIncluded(Sort(tree1, Resource('pred')),
                Sort(tree2, Resource('pred')))
        with self.assertRaises(AssertionError):
            self.assertIncluded(Sort(tree2, Resource('pred')),
                    Sort(tree1, Resource('pred')))
        with self.assertRaises(AssertionError):
            self.assertIncluded(Sort(tree1, Resource('pred')),
                    Sort(tree2, Resource('derp')))
    def testInclusionIntersectionUnionAndOr(self):
        tree1=Triple(Resource('foo'), List([Resource('a'), Resource('b')]),
                Missing())
        tree2=Triple(List([Resource('bar'), Resource('foo')]),
                List([Resource('a'), Resource('d'), Resource('b')]), Missing())
        tree3=Missing()
        for op in [Intersection,Union,And, Or]:
            self.assertIncluded(op([tree1]), op([tree2]))
            with self.assertRaises(AssertionError):
                self.assertIncluded(op([tree2]), op([tree1]))
            self.assertIncluded(op([tree1, tree3]), op([tree1, tree3]))
            self.assertIncluded(op([tree1, tree3]), op([tree3, tree1]))
            with self.assertRaises(AssertionError):
                self.assertIncluded(op([tree1, tree3]), op([tree1]))
            with self.assertRaises(AssertionError):
                self.assertIncluded(op([tree1]), op([tree3]))
    def testUnknownClass(self):
        class Foo:
            pass
        with self.assertRaises(TypeError):
            self.assertIncluded(Foo(),Foo())
