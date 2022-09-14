from functools import wraps


def cache_prev_result(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        prev = getattr(wrapped, "__history__", None)
        res = func(prev, *args, **kwargs)
        setattr(wrapped, "__history__", res)
    return wrapped
