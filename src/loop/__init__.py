import inspect
import time
from functools import wraps

from . import base


class QuitException(KeyboardInterrupt):
    """is called to break the update loop"""


def _sanity(func, *funcs):
    if not inspect.isfunction(func):
        raise TypeError('update must be a function')
    if not all([inspect.isfunction(f) for f in funcs]):
        raise TypeError('after_func must be a function')
    if func.__name__ not in ['__update__', '__setup__', '__teardown__']:
        raise ValueError('after can only be used on magic functions')


def before(*before_func):
    """decorates the update function to run the before_func before the update function"""

    def dec(func):
        _sanity(func, *before_func)

        def wrapper(*args, **kwargs):
            for _func in before_func:
                _func()
            return func(*args, **kwargs)

        return wraps(func)(wrapper)

    return dec


def after(*after_func):
    """decorates the update function to run the after_func after the update function"""

    def dec(func):
        _sanity(func, *after_func)

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for _func in after_func:
                _func()
            return result

        return wraps(func)(wrapper)

    return dec


def priority(_priority):
    """sets the priority of the update function
    higher priority means it will be called first"""

    def dec(func):
        _sanity(func)
        if func.__name__ not in ['__update__', '__setup__', '__teardown__']:
            raise ValueError('priority can only be used on magic functions')
        func.priority = _priority
        return func

    return dec


### utility functions

def set_update_rate(new_ups):
    """sets the update rate to new_ups"""
    base.UPS = new_ups


def get_update_rate():
    """returns the update rate"""
    return base.UPS


### run the loop

def run():
    """this is the main run loop"""
    for module in base.get('setup'):
        base.setup(module)
    try:
        last_tick = time.time()
        while True:
            last_tick = base._ick(last_tick)
    except KeyboardInterrupt:
        _exit()
    except Exception as e:
        print(e)
        _exit()


def _exit():
    for module in base.get('teardown'):
        base.teardown(module)
    exit()


__all__ = [
    'after',
    'before',
    'priority',
    'set_update_rate',
    'get_update_rate',
    'run',
]
