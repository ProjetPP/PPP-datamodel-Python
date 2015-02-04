import copy

from ppp_datamodel import AbstractNode, Triple, Resource, Missing
from ppp_datamodel import BooleanResource

from unittest import TestCase

class ResourceTests(TestCase):
    def testValueType(self):
        d = {'type': 'resource', 'value': 'foo', 'value-type': 'bar',
             'extra': 'baz'}
        o = AbstractNode.from_dict(d)
        self.assertEqual(o.value_type, 'bar')
        self.assertFalse(hasattr(o, 'extra'))
        self.assertRaises(AttributeError, o.get, 'extra')
        self.assertEqual(o.get('extra', strict=False), 'baz')
        self.assertEqual(o.as_dict(), d)

    def testBoolean(self):
        d = {'type': 'resource', 'value': 'true', 'value-type': 'boolean'}
        o = AbstractNode.from_dict(d)
        self.assertIsInstance(o, BooleanResource)
        self.assertEqual(o.value, True)
        self.assertEqual(o.as_dict(), d)

    def testTime(self):
        d = {'type': 'resource', 'value': '2010-05-08T23:41:54.000Z', 'value-type': 'time'}
        o = AbstractNode.from_dict(d)
        self.assertEqual(o.value, '2010-05-08T23:41:54.000Z')

    def testJsonLd(self):
        d = {
            "type": "resource",
            "value-type": "resource-jsonld",
            "value": "Douglas Adams",
            "graph": {
                "@context": "http://schema.org/",
                "@type": "Person",
                "name": {"@value": "Douglas Adams", "@language": "en"},
                "description": [
                    {"@value": "English writer and humorist", "@language": "en"},
                    {"@value": "écrivain anglais de science-fiction", "@language": "fr"}
                ],
                "sameAs": "http://www.wikidata.org/entity/Q42",
            }
        }
        o = AbstractNode.from_dict(d)
        self.assertEqual(o.value, 'Douglas Adams')
        self.assertEqual(o.graph['@context'], 'http://schema.org/')
        self.assertRaises(TypeError, hash, o)

        d2 = copy.deepcopy(d)
        d2['value'] = 'foo'
        o2 = AbstractNode.from_dict(d2)
        self.assertEqual(o, o2)
        d3 = copy.deepcopy(d)
        d3['graph']['sameAs'] = 'bar'
        o3 = AbstractNode.from_dict(d3)
        self.assertNotEqual(o, o3)
        self.assertNotEqual(o2, o3)

    def testString(self):
        self.assertRaises(TypeError, Resource, ['foo', 'bar'])
