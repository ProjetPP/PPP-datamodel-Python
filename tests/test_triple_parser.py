from unittest import TestCase

from ppp_datamodel import Triple, Resource, Missing, List, Or, And
from ppp_datamodel.parsers import parse_triples

class TripleParserTestCase(TestCase):
    def testBasics(self):
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
        self.assertEqual(parse_triples('[foo]'), List([Resource('foo')]))
        self.assertEqual(parse_triples('[(?,?,?)]'), List([
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
                        List([
                            Resource('qux')
                        ]),
                    ),
                ))

    def testOperators(self):
        t1 = And([
                Resource('foo'),
                Resource('bar'),
                ])
        self.assertEqual(parse_triples('foo /\ bar'), t1)
        self.assertEqual(parse_triples('(foo /\ bar)'), t1)
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

