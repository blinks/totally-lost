import os.path
import re
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED, NUMERIC
from whoosh.filedb.filestore import FileStorage
from whoosh import analysis, index, qparser, sorting

ROOT = 'ix'

text_analyzer = analysis.RegexTokenizer() |\
        analysis.SubstitutionFilter(r'{(\w+?)}', r'\1') |\
        analysis.StemFilter()

class Card(SchemaClass):
    name = TEXT(stored=True)
    layout = KEYWORD()
    cost = STORED()
    cmc = STORED()
    ncmc = NUMERIC(numtype=int)
    colors = KEYWORD(lowercase=True, scorable=True)
    type = KEYWORD(lowercase=True, scorable=True, stored=True)
    text = TEXT(analyzer=text_analyzer, stored=True)
    power = STORED()
    npower = NUMERIC(numtype=int)
    toughness = STORED()
    ntoughness = NUMERIC(numtype=int)
    loyalty = STORED()
    nloyalty = NUMERIC()

_schema = Card()

def create_index(storage=FileStorage(ROOT)):
    return storage.create_index(_schema)

def open_index(storage=FileStorage(ROOT)):
    return storage.open_index()

def convert(card):
    """Convert from https://mtgjson.com/documentation.html#cards to a document."""

    document = {
        'name': u' // '.join(card.get('names', [card['name']])),
        'layout': card.get('layout', u''),
        'cost': card.get('manaCost', u''),
        'colors': u' '.join(card.get('colors', [])),
        'type': card.get('type', u''),
        'text': card.get('text', u''),
    }

    non = re.compile(r'[^-+0-9.]')
    if 'cmc' in card:
        document['cmc'] = card['cmc']
        document['ncmc'] = eval(non.sub('0', card['cmc']))
    if 'power' in card:
        document['power'] = card['power']
        document['npower'] = eval(non.sub('0', card['power']))
    if 'toughness' in card:
        document['toughness'] = card['toughness']
        document['ntoughness'] = eval(non.sub('0', card['toughness']))
    if 'loyalty' in card:
        document['loyalty'] = card['loyalty']
        document['nloyalty'] = eval(non.sub('0', card['loyalty']))

    # TODO: "legalities" converted to a useful schema.

    return document

# Configure the QueryParser.
_qp = qparser.MultifieldParser(['name', 'type', 'ncmc', 'text'], schema=_schema)

def parse(query):
    return _qp.parse(query)

def search(searcher, query):
    """Returns a tuple: (results, query)"""
    q = parse(query)
    results = searcher.search(q, groupedby='ncmc', maptype=sorting.Count)
    return results, query
