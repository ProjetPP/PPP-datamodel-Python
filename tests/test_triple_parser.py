from unittest import TestCase

from ppp_datamodel import Triple, Resource, Missing, List
from ppp_datamodel.parsers import parse_triples

class TripleParserTestCase(TestCase):
    def testBasics(self):
        self.assertEqual(parse_triples('(foo, (bar, ?, (?, qux, quux)), ?)'), [
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
                )])
