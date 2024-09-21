from .redis_client import r
from json import dumps


def cache_data(data, key):
    print(f"caching data of {key}")
    r.set(key, dumps(data), ex=2592000 if key[:5] != 'today' else 30) # 30 days and 30 seconds for today's matches
    print(f"data cached for {'30 days' if key[:5] != 'today' else '30 seconds'}")
