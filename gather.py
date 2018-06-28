#!/usr/bin/env python
# Pull cards down from mtgjson.com and re-index.
import io
import json
import requests
import zipfile
import schema

URL = 'https://mtgjson.com/json/AllCards-x.json.zip'
LOCAL = 'AllCards-x.json'

def main(source):
    # Retrieve or open the file of all set data.
    raw = None
    if source.startswith('http'):
        # TODO: Cache this locally, use a timestamp check for staleness.
        print "Downloading card data."
        raw = io.BytesIO(requests.get(source).content)
    else:
        raw = open(source)

    # Unzip that file if necessary.
    jsonfile = raw
    if source.endswith('.zip'):
        print "Decompressing card data."
        jsonfile = zipfile.ZipFile(raw).open(LOCAL)

    # Index it.
    print "Indexing card data."
    index(json.load(jsonfile))

def index(data):
    """See https://mtgjson.com/documentation.html for json format."""
    ix = schema.create_index() # blow the old one away.
    writer = ix.writer()
    for card in data.values():
        writer.add_document(**schema.convert(card))
    writer.commit() # TODO: optimize=True

if __name__ == '__main__':
    main()
