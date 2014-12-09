from unittest import TestCase

from ppp_datamodel import Triple, Resource, Missing, List, Or, And, Union, Intersection
from ppp_datamodel.parsers import parse_triples, parser

class TripleParserTestCase(TestCase):
    def testBasics(self):
        self.assertEqual(parse_triples('?'), Missing())
        self.assertEqual(parse_triples('(?,?,?)'),
                Triple(Missing(), Missing(), Missing()))
        self.assertEqual(parse_triples('(?, ?, ?)'),
                Triple(Missing(), Missing(), Missing()))
    def testTriples(self):
        self.assertEqual(parse_triples('(foo, (bar, ?, (?, qux, quux)), ?)'),
                Triple(
                    Resource('foo'),
                    Triple(
                        Resource('bar'),
                        Missing(),
                        Triple(
                            Missing(),
                            Resource('qux'),
                            Resource('quux')
                            ),
                        ),
                    Missing()
                ))
    def testList(self):
        self.assertEqual(parse_triples('[]'), List([]))
        self.assertEqual(parse_triples('[foo]'), Resource('foo'))
        self.assertEqual(parse_triples('[foo, bar]'),
                List([Resource('foo'), Resource('bar')]))
        self.assertEqual(parse_triples('[(?,?,?)]'),
                Triple(
                    Missing(),
                    Missing(),
                    Missing(),
                    )
                )
        self.assertEqual(parse_triples('[foo, (?,?,?)]'), List([
                Resource('foo'),
                Triple(
                    Missing(),
                    Missing(),
                    Missing(),
                    )
                ]))
        self.assertEqual(parse_triples('(foo, [bar, (?, ?, baz)], (?, bar, [qux]))'),
                Triple(
                    Resource('foo'),
                    List([
                        Resource('bar'),
                        Triple(
                            Missing(),
                            Missing(),
                            Resource('baz'),
                            ),
                        ]),
                    Triple(
                        Missing(),
                        Resource('bar'),
                        Resource('qux'),
                    ),
                ))

    def testOperators(self):
        t1 = And([
                Resource('foo'),
                Resource('bar'),
                ])
        self.assertEqual(parse_triples(r'foo /\ bar'), t1)
        self.assertEqual(parse_triples(r'(foo /\ bar)'), t1)
        t2 = Or([
                Triple(
                    Resource('foo'),
                    Missing(),
                    Missing()
                    ),
                Triple(
                    Missing(),
                    Resource('bar'),
                    Missing()
                    )
                ])
        self.assertEqual(parse_triples('(foo, ?, ?) \/ (?, bar, ?)'), t2)
        self.assertEqual(parse_triples('((foo, ?, ?) \/ (?, bar, ?))'), t2)

    def testUnion(self):
        t = Union([
            Triple(Resource('foo'), Resource('bar'), Missing()),
            Triple(Missing(), Resource('baz'), Resource('qux')),
            ])
        self.assertEqual(parse_triples(r'(foo, bar, ?) ∪ (?, baz, qux)'), t)

    def testIntersection(self):
        t = Intersection([
            Triple(Resource('foo'), Resource('bar'), Missing()),
            Triple(Missing(), Resource('baz'), Resource('qux')),
            ])
        self.assertEqual(parse_triples(r'(foo, bar, ?) ∩ (?, baz, qux)'), t)

