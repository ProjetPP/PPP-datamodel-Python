import json
import datetime

from ppp_datamodel import AbstractNode, Triple, Resource, Missing
from ppp_datamodel import List, Union, Intersection
from ppp_datamodel import exceptions

from unittest import TestCase

T = Triple
R = Resource
M = Missing

class BaseAbstractNodeTests(TestCase):
    def testPredicateAmong(self):
        self.assertTrue(T(M(), R('foo'), M()).predicate_among(R('foo')))
        self.assertTrue(T(M(), R('bar'), M()).predicate_among([
            R('foo'), R('bar'), R('baz')]))
        self.assertFalse(T(M(), R('qux'), M()).predicate_among([
            R('foo'), R('bar'), R('baz')]))
        self.assertTrue(T(M(), R('bar'), M()).predicate_among({
            R('foo'), R('bar'), R('baz')}))
        self.assertFalse(T(M(), R('qux'), M()).predicate_among({
            R('foo'), R('bar'), R('baz')}))
        self.assertTrue(T(M(), List([R('qux'), R('bar')]), M()) \
                .predicate_among({R('foo'), R('bar'), R('baz')}))
        self.assertFalse(T(M(), List([R('qux'), R('quux')]), M()) \
                .predicate_among({R('foo'), R('bar'), R('baz')}))
        with self.assertRaises(TypeError):
            self.assertFalse(T(M(), R('foo'), M()).predicate_among('foo'))

