import os.path
import re
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED, NUMERIC
from whoosh.filedb.filestore import FileStorage
from whoosh import analysis, index, qparser, sorting

text_analyzer = analysis.RegexTokenizer() |\
        analysis.SubstitutionFilter(r'{(\w+?)}', r'\1') |\
        analysis.StemFilter()

class Card(SchemaClass):
    name = TEXT(stored=True)
    layout = KEYWORD()
    cost = STORED()
    cmc = NUMERIC(numtype=int)
    colors = KEYWORD(lowercase=True, scorable=True)
    type = KEYWORD(lowercase=True, scorable=True, stored=True)
    text = TEXT(analyzer=text_analyzer, stored=True)
    power = STORED()
    npower = NUMERIC(numtype=int)
    toughness = STORED()
    ntoughness = NUMERIC(numtype=int)
    loyalty = NUMERIC()

_schema = Card()

def create_index(storage=FileStorage('ix')):
    return storage.create_index(_schema)

def open_index(storage=FileStorage('ix')):
    return storage.open_index()

def convert(card):
    """Convert from https://mtgjson.com/documentation.html#cards to a document."""
    document = {
        'name': u' // '.join(card.get('names', [card['name']])),
        'layout': card.get('layout', u''),
        'cost': card.get('manaCost', u''),
        'cmc': int(card.get('cmc', u'0')),
        'colors': u' '.join(card.get('colors', [])),
        'type': card.get('type', u''),
        'text': card.get('text', u''),
    }

    non = re.compile(r'[^-+0-9]')
    if 'power' in card:
        document['power'] = card['power']
        document['npower'] = eval(non.sub('0', card['power']))
    if 'toughness' in card:
        document['toughness'] = card['toughness']
        document['ntoughness'] = eval(non.sub('0', card['toughness']))
    if 'loyalty' in card:
        document['loyalty'] = card['loyalty']

    # TODO: "legalities" converted to a useful schema.

    return document

# Configure the QueryParser.
_qp = qparser.MultifieldParser(['name', 'type', 'cmc', 'text'], schema=_schema)

def parse(query):
    return _qp.parse(query)

def search(searcher, query):
    """Returns a tuple: (results, query)"""
    q = parse(query)
    results = searcher.search(q, groupedby='cmc', maptype=sorting.Count)
    return results, query
