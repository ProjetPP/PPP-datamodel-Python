
from unittest import TestCase
from ppp_datamodel import Resource
from ppp_datamodel.communication import Request, Response

class RequestTest(TestCase):
    def testEquality(self):
        self.assertEqual(Request('en', 1, Resource(value='foo')),
                         Request('en', 1, Resource(value='foo')))
        self.assertNotEqual(Request('en', 1, Resource(value='foo')),
                            Request('en', 1, Resource(value='bar')))
