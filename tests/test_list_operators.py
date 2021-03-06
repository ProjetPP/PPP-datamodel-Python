from ppp_datamodel import AbstractNode, Resource, List, Triple, Missing
from ppp_datamodel import Union, first, Nth, Exists

from unittest import TestCase

class ListOperatorTests(TestCase):
    def testListNodesType(self):
        d1 = {"type": "sort", "predicate": {"type": "resource", "value": "foo"},
              "list": [{"type": "resource", "value": "George Washington"},
                       {"type": "resource", "value": "Theodore Roosevelt"}]}
        self.assertRaises(TypeError, AbstractNode.from_dict, d1)
        d2 = {"type": "union",
              "list": [{"type": "resource", "value": "George Washington"},
                       {"type": "resource", "value": "Theodore Roosevelt"}]}
        AbstractNode.from_dict(d2)
        d3 = {"type": "sort", "predicate": {"type": "resource", "value": "foo"},
              "list": {"type": "resource", "value": "George Washington"}}
        AbstractNode.from_dict(d3)
    def testUnion(self):
        d1 = {"type": "union",
              "list": [{"type": "resource", "value": "George Washington"},
                       {"type": "resource", "value": "Theodore Roosevelt"}]}
        d2 = {"type": "union",
              "list": [{"type": "list", "list": [{"type": "resource", "value": "George Washington"}]},
                       {"type": "list", "list": [{"type": "resource", "value": "Theodore Roosevelt"}]}]}
        o1 = AbstractNode.from_dict(d1)
        o2 = AbstractNode.from_dict(d2)
        self.assertEqual(o1.as_dict(), d1)
        self.assertEqual(o2.as_dict(), d2)
        self.assertEqual(o1.list[0], Resource('George Washington'))
        o1.as_json()

    def testHash(self):
        o1 = List([Resource('foo'), Resource('bar')])
        o2 = List([Resource('foo'), Resource('bar')])
        h1 = hash(o1)
        h2 = hash(o2)
        self.assertEqual(h1, h2)
        o1.list.append(Resource('baz'))
        self.assertNotEqual(hash(o1), h2)
        hash(Union([o1, o2]))
        o1.as_json()

    def testFirst(self):
        first(List([Resource('foo'), Resource('bar')]))

    def testTraverseNoException(self):
        def pred(node):
            return node
        Union([List([Resource('foo')]), List([Resource('bar')])]).traverse(pred)
        first(List([Resource('foo'), Resource('bar')])).traverse(pred)
        Exists(List([Resource('foo'), Resource('bar')])).traverse(pred)
        Exists(Resource('foo')).traverse(pred)

    def testTraverseOrder(self):
        def pred(node):
            if isinstance(node, Exists):
                self.assertEqual(node.list, Resource('baz'))
                return Resource('qux')
            elif isinstance(node, List):
                self.assertEqual(node.list, [Resource('bar')])
                return Resource('baz')
            elif isinstance(node, Resource):
                return Resource('bar')
            else:
                assert False, node
        self.assertEqual(Exists(Resource('foo')).traverse(pred),
                Resource('qux'))

    def testTraverseReturnTriple(self):
        def pred(node):
            if isinstance(node, Exists):
                return Resource('qux')
            elif isinstance(node, List):
                return Triple(Resource('baz'), Missing(), Missing())
            elif isinstance(node, Resource):
                return Resource('bar')
            else:
                assert False, node
        self.assertEqual(Exists(Resource('foo')).traverse(pred),
                Resource('qux'))
