from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/<name>')
def hello(name):
    return jsonify(name=name)
