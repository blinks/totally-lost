#!/usr/bin/env python3
# Pull cards down from mtgjson.com and re-index.
import io
import json
import os.path
import os
import requests
import schema
import zipfile

URL = 'https://mtgjson.com/json/AllCards.json.zip'
LOCAL = 'AllCards.json'

def main():
    # Retrieve or open the file of all set data.
    # TODO: Cache this locally, use a timestamp check for staleness.
    print("Downloading card data.")
    raw = io.BytesIO(requests.get(URL).content)

    # Unzip that file if necessary.
    print("Decompressing card data.")
    jsonfile = zipfile.ZipFile(raw).open(LOCAL)

    # Index it.
    print("Indexing card data.")
    os.path.isdir(schema.ROOT) or os.makedirs(schema.ROOT)
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
