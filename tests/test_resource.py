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

    def testGeojson(self):
        d = {
                "type": "resource",
                "value": "+125.6, +10.1",
                "geojson": {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [125.6, 10.1]},
                    "properties": {"name": "Dinagat Islands"}
                },
                "value-type": "geo-json"
            }
        o = AbstractNode.from_dict(d)
        self.assertEqual(o.geojson['type'], 'Feature')
        hash(o)
