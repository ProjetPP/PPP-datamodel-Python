from unittest import TestCase

from ppp_datamodel import Triple, Resource, Missing
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
