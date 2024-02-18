from flask import Flask, jsonify, make_response
from scrape.index import scrape
import re
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.json.sort_keys = False

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour",
                    "20 per minute", "5 per second"],
    storage_uri="memory://",
)


@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
        jsonify(error=f"ratelimit exceeded {e.description}"), 429
    )


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
