from functools import wraps


def cache_first_res(func):
    """
    Cache the first result, then return it afterwards.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        cache = getattr(wrapped, "__return_cache__", None)
        if cache is not None:
            return cache
        res = func(*args, **kwargs)
        setattr(wrapped, "__return_cache__", res)
    return wrapped


def cache_prev_result(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        prev = getattr(wrapped, "__history__", None)
        res = func(prev, *args, **kwargs)
        setattr(wrapped, "__history__", res)
    return wrapped
