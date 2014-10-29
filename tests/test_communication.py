
import json
from unittest import TestCase
from ppp_datamodel import Resource, Missing
from ppp_datamodel.communication import Request, TraceItem, Response

class RequestTest(TestCase):
    def testEquality(self):
        self.assertEqual(Request('1', 'en', {}, [], Resource(value='foo')),
                         Request('1', 'en', {}, [], Resource(value='foo')))
        self.assertNotEqual(Request('1', 'en', {}, [], Resource(value='foo')),
                            Request('1', 'en', {}, [], Resource(value='bar')))

    def testRepr(self):
        r="<ppp_datamodel.Request(id='1', language='en', tree=<PPP node \"resource\" {'value': 'foo'}>, sentence=None, measures={}, trace=[])>"
        self.assertEqual(repr(Request('1', 'en', {}, [], Resource(value='foo'))), r)

    def testFromJson(self):
        j = {'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
             'tree': {'type': 'resource', 'value': 'foo'}}
        self.assertEqual(Request('1', 'en', {}, [], Resource(value='foo')),
                         Request.from_dict(j))
        self.assertEqual(Request('1', 'en', {}, [], Resource(value='foo')),
                         Request.from_json(json.dumps(j)))
        self.assertEqual(json.loads(Request.from_dict(j).as_json()), j)

class ResponseTest(TestCase):
    def testEquality(self):
        self.assertEqual(Response('en', Resource(value='foo'), {}, []),
                         Response('en', Resource(value='foo'), {}, []))
        self.assertNotEqual(Response('en', Resource(value='foo'), {}, []),
                            Response('en', Resource(value='bar'), {}, []))
        self.assertNotEqual(Response('en', Resource(value='foo'), {'accuracy': 0.5}, []),
                            Response('en', Resource(value='foo'), {'accuracy': 0.6}, []))

    def testRepr(self):
        r="<PPP response language='en', tree=<PPP node \"resource\" {'value': 'foo'}>, measures={}, trace=[]>"
        self.assertEqual(repr(Response('en', Resource(value='foo'), {}, [])), r)

    def testFromJson(self):
        r = {'language': 'en', 'measures': {},
             'trace': [{'module': 'foo', 'tree': {'type': 'missing'}, 'measures': {}}],
             'tree': {'type': 'resource', 'value': 'foo'}}
        t = [TraceItem('foo', Missing(), {})]
        self.assertEqual(Response('en', Resource(value='foo'), {}, t),
                         Response.from_json(json.dumps(r)))
        self.assertEqual(Response('en', Resource(value='foo'), {}, t),
                         Response.from_dict(r))
        self.assertEqual(Response('en', Resource(value='foo'), {}, t),
                         Response.from_json(json.dumps(r)))
        self.assertEqual(json.loads(Response.from_dict(r).as_json()), r)

