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
    def testPredicateSet(self):
        self.assertEqual(T(M(), R('foo'), M()).predicate_set,
                {R('foo')})
        self.assertEqual(T(M(), List([R('foo'), R('bar')]), M()).predicate_set,
                {R('foo'), R('bar')})
