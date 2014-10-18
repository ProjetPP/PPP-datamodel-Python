
import json
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

    def testRepr(self):
        r="<PPP request language='en', tree=<PPP node \"resource\" {'value': 'foo'}>>"
        self.assertEqual(repr(Request('en', Resource(value='foo'))), r)

    def testFromJson(self):
        j = {'language': 'en',
             'tree': {'type': 'resource', 'value': 'foo'}}
        self.assertEqual(Request('en', Resource(value='foo')),
                         Request.from_json(j))
        self.assertEqual(Request('en', Resource(value='foo')),
                         Request.from_json(json.dumps(j)))
        self.assertEqual(Request.from_json(j).as_json(), json.dumps(j))

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

    def testRepr(self):
        r="<PPP response language='en', pertinence=0.5, tree=<PPP node \"resource\" {'value': 'foo'}>>"
        self.assertEqual(repr(Response('en', 0.5, Resource(value='foo'))), r)

    def testFromJson(self):
        r = {'language': 'en', 'pertinence': 0.5,
             'tree': {'type': 'resource', 'value': 'foo'}}
        self.assertEqual(Response('en', 0.5, Resource(value='foo')),
                         Response.from_json(r))
        self.assertEqual(Response('en', 0.5, Resource(value='foo')),
                         Response.from_json(json.dumps(r)))
        self.assertEqual(Response.from_json(r).as_json(), json.dumps(r))
