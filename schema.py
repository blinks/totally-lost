import os.path
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
from whoosh.qparser import QueryParser
from whoosh import index

class Card(SchemaClass):
    name = TEXT(stored=True)
    rules_text = TEXT(stored=True)
    card_type = KEYWORD(stored=True)

_schema = Card()
_qp = QueryParser('rules_text', schema=_schema)

def create_index(path='ix'):
    if not os.path.exists(path):
        os.mkdir(path)
    return index.create_in(path, _schema)

def open_index(path='ix'):
    return index.open_dir(path)

def parse(query):
    return _qp.parse(query)
