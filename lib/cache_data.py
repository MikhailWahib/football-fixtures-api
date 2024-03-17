from lib.redis_client import r
from datetime import datetime, timedelta
import json


def cache_data(data, data_date_string):
    current_date = datetime.now().date()
    data_date = datetime.strptime(data_date_string, '%Y-%m-%d').date()
    diff = data_date - current_date

    if diff.days < 0:
        two_weeks_ago_date = current_date - timedelta(days=15)
        expiry_date = data_date - two_weeks_ago_date
        expiry_time = expiry_date.days * 86400

        print(two_weeks_ago_date)

        r.set(data_date_string, json.dumps(
            data), ex=expiry_time)

        print('data cached for', expiry_date.days, 'days')

    elif diff.days >= 1:
        expiry_date = data_date - current_date
        expiry_time = expiry_date.days * 86400

        r.set(data_date_string, json.dumps(
            data), ex=expiry_time)

        print('data cached for', expiry_date.days, 'days')
