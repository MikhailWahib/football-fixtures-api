from flask import Flask, jsonify
from scrape.index import scrape
import re
from datetime import datetime

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
    data = scrape()

    error_message = handle_error_response(data)

    if error_message:
        return error_message

    return jsonify({
        "leagues": data
    })


# /yy-mm-dd
@app.route('/<date>')
def date(date):
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        return jsonify({
            "error": "Invalid date format, should be yy-mm-dd"
        }), 400

    current_date = datetime.today().strftime('%Y-%m-%d')

    if date == current_date:
        return jsonify({
            "error": "For today's fixtures, use '/today' endpoint"
        }), 400

    data = scrape(f'/{date}')

    error_message = handle_error_response(data)

    if error_message:
        return error_message

    return jsonify({
        "leagues": data
    })


if __name__ == '__main__':
    app.run(debug=True)
