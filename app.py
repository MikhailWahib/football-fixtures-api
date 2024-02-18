from flask import Flask, jsonify
from scrape.index import scrape
import re
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/')
def hello():
    return jsonify({
        "hello": "world"
    })


def handle_error_response(data):
    if data is None:
        return jsonify({
            "error": "Something went wrong"
        }), 500


'''
if no data it returns an empty list
if there is an error it returns an error message with a 500 status code
'''


@app.route('/today')
def index():
    data = scrape('https://www.bbc.com/sport/football/scores-fixtures')

    error_message = handle_error_response(data)

    if error_message:
        return error_message

    return jsonify({
        "leagues": data
    })


# /mm-dd
@app.route('/<date>')
def date(date):
    if not re.match(r'^\d{2}-\d{2}$', date):
        return jsonify({
            "error": "Invalid date format, should be mm-dd"
        }), 400

    data = scrape(
        f'https://www.bbc.com/sport/football/scores-fixtures/2024-{date}')

    error_message = handle_error_response(data)

    if error_message:
        return error_message

    return jsonify({
        "leagues": data
    })
