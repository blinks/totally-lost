#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
from flask import Flask, Markup, render_template, request, send_from_directory
import re
import schema
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search")
def search():
    query = request.args.get('q', '')
    ix = schema.open_index() # TODO: open once in prod
    with ix.searcher() as searcher:
        results, query = schema.search(searcher, query)
        return render_template('results.html', query=query, results=results)

@app.route("/fonts/<path:path>")
def fonts(path):
    return send_from_directory('static/fonts', path)

@app.template_filter("para")
def split_paragraphs(s):
    # Split into paragraphs.
    s = u'<p>%s</p>' % u'</p><p>'.join(s.split(u'\n'))
    return Markup(symbolize(s))

@app.template_filter("symbolize")
def symbolize(s):
    # Italicize reminder text.
    s = re.sub(r'\((.+?)\)', r'(<i>\1</i>)', s)

    # Substitute icons for symbol text, provided by andrewgioia/Mana
    # https://andrewgioia.github.io/Mana/icons.html
    def symrepl(m):
        key = m.group(1).lower()
        suffix = 'ms-cost'
        if key == 't':
            key = 'tap'
        elif key == 'chaos':
            suffix = ''
        return '<i class="ms ms-%s %s"></i>' % (key, suffix)
    s = re.sub(r'{(.+?)}', symrepl, s)

    return Markup(s) # disable auto-escape.

if __name__ == '__main__':
    app.run(host='0.0.0.0')
