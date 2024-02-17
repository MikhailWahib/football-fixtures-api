from flask import Flask, jsonify
from scrape.index import scrape

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/')
def hello():
    return jsonify({
        "hello": "world"
    })


@app.route('/today')
def index():
    data = scrape('https://www.bbc.com/sport/football/scores-fixtures')
    return jsonify({
        "leagues": data
    })
