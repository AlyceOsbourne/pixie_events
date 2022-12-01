import cProfile
import pstats
from functools import wraps

pr = cProfile.Profile()


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('cumulative')
        ps.print_stats()
        return result
    return wrapper
