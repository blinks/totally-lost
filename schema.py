import os.path
import re
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED, NUMERIC
from whoosh.qparser import MultifieldParser
from whoosh import index

class Card(SchemaClass):
    name = TEXT(stored=True)
    layout = STORED()
    cost = STORED()
    cmc = NUMERIC(numtype=int, decimal_places=2)
    type = KEYWORD(stored=True)
    text = TEXT(stored=True)
    power = STORED()
    npower = NUMERIC(numtype=int, decimal_places=2)
    toughness = STORED()
    ntoughness = NUMERIC(numtype=int, decimal_places=2)
    loyalty = NUMERIC()

_schema = Card()
_qp = MultifieldParser(['name', 'type', 'text'], schema=_schema)

def create_index(path='ix'):
    if not os.path.exists(path):
        os.mkdir(path)
    return index.create_in(path, _schema)

def open_index(path='ix'):
    return index.open_dir(path)

def convert(card):
    """Convert from https://mtgjson.com/documentation.html#cards to a document."""
    document = {
        'name': u' // '.join(card.get('names', [card['name']])),
        'layout': card.get('layout', u''),
        'cost': card.get('manaCost', u''),
        'cmc': float(card.get('cmc', u'0')),
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

def parse(query):
    return _qp.parse(query)
