import json

from ppp_datamodel import AbstractNode, Triple
from ppp_datamodel import exceptions

from unittest import TestCase

class BaseAbstractNodeTests(TestCase):
    def testAbstract(self):
        self.assertRaises(TypeError, AbstractNode)

    def testBasicConstructor(self):
        n = Triple(subject='s', predicate='p', object='o')
        self.assertEqual(n.subject, 's')
        self.assertEqual(n['subject'], 's')
        self.assertRaises(AttributeError, lambda: n.foobar)

    def testEmptyConstructor(self):
        n = Triple()
        self.assertRaises(exceptions.AttributeNotProvided,
            lambda: n.predicate)

    def testInvalidConstrutorAttribute(self):
        self.assertRaises(TypeError, Triple, foo='bar')

    def testToJsonPerfect(self):
        n = Triple(subject='s', predicate='p', object='o')
        self.assertEqual(json.loads(n.as_json()), {'type': 'triple',
            'subject': 's', 'predicate': 'p', 'object': 'o'})

    def testToJsonMissing(self):
        n = Triple(subject='s', predicate='p')
        self.assertEqual(json.loads(n.as_json()), {'type': 'triple',
            'subject': 's', 'predicate': 'p'})

    def testToJsonNone(self):
        n = Triple(subject='s', predicate='p', object=None)
        self.assertEqual(json.loads(n.as_json()), {'type': 'triple',
            'subject': 's', 'predicate': 'p', 'object': None})

    def testFromJsonPerfect(self):
        d = {'type': 'triple',
            'subject': 's', 'predicate': 'p', 'object': 'o'}
        self.assertIsInstance(AbstractNode.from_json(d), Triple)
        self.assertEqual(d, json.loads(AbstractNode.from_json(d).as_json()))
        self.assertEqual(d, json.loads(AbstractNode.from_json(json.dumps(d)).as_json()))

    def testFromJsonMissing(self):
        d = {'type': 'triple',
            'subject': 's', 'predicate': 'p'}
        n = AbstractNode.from_json(d)
        self.assertEqual(d, json.loads(n.as_json()))
        self.assertEqual(n.predicate, 'p')
        self.assertNotIn('object', n)

    def testFromJsonNone(self):
        d = {'type': 'triple',
            'subject': 's', 'predicate': 'p', 'object': None}
        n = AbstractNode.from_json(d)
        self.assertEqual(d, json.loads(n.as_json()))
        self.assertIn('object', n)
        self.assertEqual(n.object, None)

    def testFromJsonTypeNotProvided(self):
        d = {'subject': 's', 'predicate': 'p', 'object': None}
        self.assertRaises(exceptions.AttributeNotProvided,
                AbstractNode.from_json, d)

    def testFromJsonTypeInvalid(self):
        d = {'type': 'foobar',
            'subject': 's', 'predicate': 'p', 'object': None}
        self.assertRaises(exceptions.UnknownNodeType,
                AbstractNode.from_json, d)
