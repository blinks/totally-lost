# Totally Lost
Magic: The Gathering index and search.

## Development

```
pip install Flask requests Whoosh
FLASK_APP=lost.py flask run
```

- Flask (simple http server) docs: http://flask.pocoo.org/
- Requests (simple http requests) docs: http://requests.readthedocs.io/
- Whoosh (pure-python indexing) docs: https://whoosh.readthedocs.io/

### Organization

- `lost.py` is the http router, with urls paired up with their effects.
- `schema.py` contains everything schema-related, including methods for
	creating and opening indexes and parsing the query. If it needs details about
	the schema to work, put it there.
- `gather.py` is the executable script that generates a new index.
