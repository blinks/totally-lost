# vim: set fileencoding=utf-8 :
import json
import schema
import unittest
from whoosh.filedb.filestore import RamStorage
from cStringIO import StringIO

# Pulled direct from AllCards-x.json
JSON = None
with open('AllCards-x.json', 'r') as data:
    JSON = json.load(data)


class SchemaTest(unittest.TestCase):
    def setUp(self):
        self.ix = schema.create_index(RamStorage())
        self._index('Birds of Paradise')

    def tearDown(self):
        if self.searcher is not None:
            self.searcher.close()

    def _index(self, *names):
        writer = self.ix.writer()
        for card in JSON.values():
            if card['name'] in names:
                writer.add_document(**schema.convert(card))
        writer.commit()

    def _search(self, query):
        self.searcher = self.ix.searcher()
        return schema.search(self.searcher, query)

    def test_birds_of_paradise(self):
        """Smoke test that a specific card is returned for its name."""
        res, query = self._search('birds of paradise')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['name'], u'Birds of Paradise')
        self.assertEqual(res[0]['type'], u'Creature \u2014 Bird')
        self.assertEqual(res[0]['power'], u'0')
        self.assertEqual(res[0]['toughness'], u'1')
        self.assertRegexpMatches(res[0]['text'],
                u'^Flying\n{T}: Add one mana of any color')


if __name__ == '__main__':
    unittest.main()
