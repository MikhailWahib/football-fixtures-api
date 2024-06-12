from .redis_client import r
from json import dumps


def cache_data(data, data_date_string='today'):
    r.set(data_date_string, dumps(data), ex=2592000 if data_date_string != 'today' else 30) # 30 days and 30 seconds for today's matches
    print(f"data cached for {'30 days' if data_date_string != 'today' else '30 seconds'}")
