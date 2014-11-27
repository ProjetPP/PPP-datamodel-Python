from ppp_datamodel import AbstractNode, Resource
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
