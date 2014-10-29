import json

from ppp_datamodel import AbstractNode, Triple, Resource, Missing
from ppp_datamodel import exceptions

from unittest import TestCase

R = Resource
r = lambda x:{'type': 'resource', 'value': x}
M = Missing
m = lambda:{'type': 'missing'}

class BaseAbstractNodeTests(TestCase):
    def testAbstract(self):
        self.assertRaises(TypeError, AbstractNode)

    def testBasicConstructor(self):
        n = Triple(subject=R('s'), predicate=R('p'), object=R('o'))
        self.assertEqual(n.subject, R('s'))
        self.assertEqual(n['subject'], R('s'))
        self.assertRaises(AttributeError, lambda: n.foobar)

    def testEmptyConstructor(self):
        n = Triple()
        self.assertRaises(exceptions.AttributeNotProvided,
            lambda: n.predicate)

    def testInvalidConstrutorAttribute(self):
        self.assertRaises(TypeError, Triple, foo='bar')

    def testToJsonPerfect(self):
        n = Triple(subject=R('s'), predicate=R('p'), object=R('o'))
        self.assertEqual(json.loads(n.as_json()), {'type': 'triple',
            'subject': r('s'), 'predicate': r('p'), 'object': r('o')})

    def testToJsonMissing(self):
        n = Triple(subject=R('s'), predicate=R('p'))
        self.assertEqual(json.loads(n.as_json()), {'type': 'triple',
            'subject': r('s'), 'predicate': r('p')})

    def testToJsonNone(self):
        n = Triple(subject=R('s'), predicate=R('p'), object=Missing())
        self.assertEqual(json.loads(n.as_json()), {'type': 'triple',
            'subject': r('s'), 'predicate': r('p'), 'object': m()})

    def testFromJsonPerfect(self):
        d = {'type': 'triple',
            'subject': r('s'), 'predicate': r('p'), 'object': r('o')}
        self.assertIsInstance(AbstractNode.from_dict(d), Triple)
        self.assertIsInstance(AbstractNode.from_json(json.dumps(d)), Triple)
        self.assertEqual(d, json.loads(AbstractNode.from_dict(d).as_json()))
        self.assertEqual(d, json.loads(AbstractNode.from_json(json.dumps(d)).as_json()))

    def testFromJsonMissing(self):
        d = {'type': 'triple',
            'subject': r('s'), 'predicate': r('p')}
        n = AbstractNode.from_dict(d)
        self.assertEqual(d, json.loads(n.as_json()))
        self.assertEqual(n.predicate, r('p'))
        self.assertNotIn('object', n)

    def testFromJsonNone(self):
        d = {'type': 'triple',
             'subject': r('s'), 'predicate': r('p'), 'object': m()}
        n = AbstractNode.from_dict(d)
        self.assertEqual(d, json.loads(n.as_json()))
        self.assertIn('object', n)
        self.assertEqual(n.object, M())

    def testFromJsonTypeNotProvided(self):
        d = {'subject': r('s'), 'predicate': r('p'), 'object': m()}
        self.assertRaises(exceptions.AttributeNotProvided,
                AbstractNode.from_dict, d)

    def testFromJsonTypeInvalid(self):
        d = {'type': 'foobar',
            'subject': r('s'), 'predicate': r('p'), 'object': m()}
        self.assertRaises(exceptions.UnknownNodeType,
                AbstractNode.from_dict, d)

    def testCheckType(self):
        self.assertRaises(TypeError, Triple, {})

    def testEq(self):
        self.assertEqual(Missing(), Missing())
        self.assertEqual(Resource('foo'), Resource('foo'))
        self.assertNotEqual(Missing(), Resource('foo'))
        self.assertEqual(Missing(), {'type': 'missing'})
        self.assertNotEqual(Missing(), {'type': 'missing', 'f': 'b'})
        self.assertEqual(Resource('foo'), {'type': 'resource',
                                           'value': 'foo'})
        self.assertNotEqual(Missing(), '')
