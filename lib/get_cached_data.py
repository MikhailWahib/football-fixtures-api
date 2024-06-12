from .redis_client import r
import json


def get_cached_data(url, data_date_string='today'):
    if r.get(data_date_string):
        print(f"Cache hit for data of {data_date_string}")
        return json.loads(r.get(data_date_string))
