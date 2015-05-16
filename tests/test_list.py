from ppp_datamodel import AbstractNode, Resource, List, Triple, Missing
from ppp_datamodel import Union, first, Nth, Exists

from unittest import TestCase

R = Resource

class ListTests(TestCase):
    def testEquality(self):
        self.assertEqual(List([R('foo'), R('bar')]), List([R('foo'), R('bar')]))
        self.assertNotEqual(List([R('foo'), R('bar')]), List([R('foo'), R('baz')]))
        self.assertEqual(List([R('foo')]), List([R('foo')]))
        self.assertEqual(List([R('foo')]), R('foo'))
        self.assertNotEqual(List([R('foo')]), R('bar'))
        self.assertEqual(R('foo'), List([R('foo')]))
        self.assertNotEqual(R('bar'), List([R('foo')]))

