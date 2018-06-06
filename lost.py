from flask import Flask, render_template, request
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
        results = searcher.search(schema.parse(query))
        return render_template('results.html', query=query, results=results)
