from lib.redis_client import r
import json


def get_cached_data(url, data_date_string):
    if r.get(data_date_string):
        print(f"Using cached data for {data_date_string}")
        return json.loads(r.get(data_date_string))
