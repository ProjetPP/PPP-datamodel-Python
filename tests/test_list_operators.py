from ppp_datamodel import AbstractNode, Resource, List
from ppp_datamodel import Union

from unittest import TestCase

class ListOperatorTests(TestCase):
    def testUnion(self):
        d1 = {"type": "union",
              "list": [{"type": "resource", "value": "George Washington"},
                       {"type": "resource", "value": "Theodore Roosevelt"}]}
        d2 = {"type": "union",
              "list": [[{"type": "resource", "value": "George Washington"}],
                       [{"type": "resource", "value": "Theodore Roosevelt"}]]}
        o1 = AbstractNode.from_dict(d1)
        o2 = AbstractNode.from_dict(d2)
        self.assertEqual(o1, o2)
        self.assertEqual(o1.as_dict(), d2)
        self.assertEqual(o2.as_dict(), d2)
        self.assertEqual(o1.list[0], [Resource('George Washington')])

    def testHash(self):
        o1 = List([Resource('foo'), Resource('bar')])
        o2 = List([Resource('foo'), Resource('bar')])
        h1 = hash(o1)
        h2 = hash(o2)
        self.assertEqual(h1, h2)
        o1.list.append(Resource('baz'))
        self.assertNotEqual(hash(o1), h2)
