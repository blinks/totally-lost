#!/usr/bin/env python
# Pull cards down from mtgjson.com and re-index.
import io
import json
import requests
import zipfile
import schema

URL = 'https://mtgjson.com/json/AllSets.json.zip'
LOCAL = 'AllSets.json'

def main(source):
    # Retrieve or open the file of all set data.
    raw = None
    if source.startswith('http'):
        # TODO: Cache this locally, use a timestamp check for staleness.
        raw = io.BytesIO(requests.get(source).content)
    else:
        raw = open(source)

    # Unzip that file if necessary.
    jsonfile = raw
    if source.endswith('.zip'):
        jsonfile = zipfile.ZipFile(raw).open('AllSets.json')

    # Index it.
    index(json.load(jsonfile))

def index(data):
    """See https://mtgjson.com/documentation.html for json format."""
    ix = schema.create_index() # blow the old one away.
    writer = ix.writer()
    for code in data:
        for card in data[code]['cards']:
            writer.add_document(
                    name=card['name'],
                    card_type=card.get('type', u''),
                    rules_text=card.get('text', u''))
    writer.commit() # TODO: optimize=True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    # As arguments are added here, pass them to main as keyword args.
    parser.add_argument('source', metavar='URL', type=str, default=URL)
    args = parser.parse_args()
    main(args.source)
