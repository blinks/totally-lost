import os.path
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
from whoosh.qparser import MultifieldParser
from whoosh import index

class Card(SchemaClass):
    name = TEXT(stored=True)
    type = KEYWORD(stored=True)
    text = TEXT(stored=True)

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
    return {
        'name': u' // '.join(card.get('names', [card['name']])),
        'type': card.get('type', u''),
        'text': card.get('text', u''),
    }

def parse(query):
    return _qp.parse(query)
