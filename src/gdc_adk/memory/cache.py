_CACHE = {}

def get_cached(key):
    return _CACHE.get(key)

def set_cached(key, value):
    _CACHE[key] = value
