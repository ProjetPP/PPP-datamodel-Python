
import json
from unittest import TestCase
from ppp_datamodel import Resource, Missing
from ppp_datamodel.communication import Request, TraceItem, Response

class RequestTest(TestCase):
    def testEquality(self):
        self.assertEqual(Request('1', 'en', Resource(value='foo'), {}, []),
                         Request('1', 'en', Resource(value='foo'), {}, []))
        self.assertNotEqual(Request('1', 'en', Resource(value='foo'), {}, []),
                            Request('1', 'en', Resource(value='bar'), {}, []))

    def testFromJson(self):
        j = {'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
             'tree': {'type': 'resource', 'value': 'foo'}}
        self.assertEqual(Request('1', 'en', Resource(value='foo'), {}, []),
                         Request.from_dict(j))
        self.assertEqual(Request('1', 'en', Resource(value='foo'), {}, []),
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

    def testFromJson(self):
        r = {'language': 'en', 'measures': {},
             'trace': [{'module': 'foo', 'tree': {'type': 'missing'}, 'measures': {},
                 'times': {}}],
             'tree': {'type': 'resource', 'value': 'foo'}}
        t = [TraceItem('foo', Missing(), {}, {})]
        self.assertEqual(Response('en', Resource(value='foo'), {}, t),
                         Response.from_json(json.dumps(r)))
        self.assertEqual(Response('en', Resource(value='foo'), {}, t),
                         Response.from_dict(r))
        self.assertEqual(Response('en', Resource(value='foo'), {}, t),
                         Response.from_json(json.dumps(r)))
        self.assertEqual(json.loads(Response.from_dict(r).as_json()), r)

    def testFromLegacyJson(self):
        r1 = {'language': 'en', 'measures': {},
             'trace': [{'module': 'foo', 'tree': {'type': 'missing'}, 'measures': {}}],
             'tree': {'type': 'resource', 'value': 'foo'}}
        r2 = {'language': 'en', 'measures': {},
             'trace': [{'module': 'foo', 'tree': {'type': 'missing'}, 'measures': {},
                 'times': {}}],
             'tree': {'type': 'resource', 'value': 'foo'}}
        t = [TraceItem('foo', Missing(), {}, {})]
        self.assertEqual(Response('en', Resource(value='foo'), {}, t),
                         Response.from_json(json.dumps(r1)))
        self.assertEqual(Response('en', Resource(value='foo'), {}, t),
                         Response.from_dict(r1))
        self.assertEqual(Response('en', Resource(value='foo'), {}, t),
                         Response.from_json(json.dumps(r1)))
        self.assertEqual(json.loads(Response.from_dict(r1).as_json()), r2)

class TraceItemTest(TestCase):
    def testFromDict(self):
        d = {'tree': {'type': 'missing'}, 'module': 'foo', 'measures': {}, 'times': {}}
        self.assertEqual(TraceItem.from_dict(d),
                TraceItem('foo', Missing(), {}, {}))

