from unittest import TestCase

from ppp_datamodel import Resource, Triple, Missing, Intersection, Union, List, Union, And, Or, Exists, First, Last, Sort
from ppp_datamodel import utils

T = Triple
R = Resource
M = Missing

class UtilsTests(TestCase):
    def testContainsMissing(self):
        f = utils.contains_missing
        self.assertTrue(f(T(subject=R(value='foo'), object=T(subject=M()))))
        self.assertFalse(f(T(subject=R(value='foo'), object=T(subject=R()))))
        self.assertTrue(f(M()))
    def testInclusionBasic(self):
        f = utils.isincluded
        self.assertTrue(f(Missing(),Missing()))
        self.assertTrue(f(Resource('foo'),Resource('foo')))
        self.assertFalse(f(Resource('foo'),Resource('bar')))
        self.assertTrue(f(List([Resource('foo')]),Resource('foo')))
        self.assertFalse(f(List([Resource('foo')]),Resource('bar')))
        self.assertTrue(f(Resource('foo'),List([Resource('foo')])))
        self.assertFalse(f(Resource('foo'),List([Resource('bar')])))
        self.assertTrue(f(List([Resource('foo')]),List([Resource('foo')])))
        self.assertFalse(f(List([Resource('foo')]),List([Resource('bar')])))
        self.assertTrue(f(List([Resource('foo')]),List([Resource('foo'),Resource('bar')])))
        self.assertFalse(f(List([Resource('foo'),Resource('bar')]),List([Resource('foo')])))
    def testInclusionDifferentType(self):
        f = utils.isincluded
        l = [Resource('foo'),Missing(),Triple(Resource('foo'),Resource('foo'),Resource('foo')),\
            Intersection([Resource('foo')]), Union([Resource('foo')]),\
            And([Resource('foo')]), Or([Resource('foo')]), Exists(Resource('foo')),\
            First(Resource('foo')), Last(Resource('foo')), Sort(Resource('foo'),'pred')]
        for t1 in l:
            for t2 in l:
                if type(t1) == type(t2):
                    break
                self.assertFalse(f(t1,t2))
