
from unittest import TestCase
from ppp_datamodel import Resource
from ppp_datamodel.communication import Request, Response

class RequestTest(TestCase):
    def testEquality(self):
        self.assertEqual(Request('en', Resource(value='foo')),
                         Request('en', Resource(value='foo')))
        self.assertNotEqual(Request('en', Resource(value='foo')),
                            Request('en', Resource(value='bar')))
        self.assertEqual(Request('en', Resource(value='foo')),
                         {'language': 'en',
                          'tree': {'type': 'resource', 'value': 'foo'}})
        self.assertNotEqual(Request('en', Resource(value='foo')),
                            {'language': 'en',
                             'tree': {'type': 'resource', 'value': 'bar'}})

class ResponseTest(TestCase):
    def testEquality(self):
        self.assertEqual(Response('en', 1, Resource(value='foo')),
                         Response('en', 1, Resource(value='foo')))
        self.assertNotEqual(Response('en', 1, Resource(value='foo')),
                            Response('en', 1, Resource(value='bar')))
        self.assertEqual(Response('en', 1, Resource(value='foo')),
                         {'language': 'en', 'pertinence': 1,
                          'tree': {'type': 'resource', 'value': 'foo'}})
        self.assertNotEqual(Response('en', 1, Resource(value='foo')),
                            {'language': 'en', 'pertinence': 1,
                             'tree': {'type': 'resource', 'value': 'bar'}})
