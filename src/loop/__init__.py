import inspect
import time
from functools import wraps

from .base import *


class QuitException(Exception):
    """is called to break the update loop"""


def before(*before_func):
    """decorates the update function to run the before_func before the update function"""

    def dec(func):
        if not inspect.isfunction(func):
            raise TypeError('update must be a function')
        if not all([inspect.isfunction(f) for f in before_func]):
            raise TypeError('before_func must be a function')

        def wrapper(*args, **kwargs):
            for _func in before_func:
                _func()
            return func(*args, **kwargs)

        return wraps(func)(wrapper)

    return dec


def after(*after_func):
    """decorates the update function to run the after_func after the update function"""

    def dec(func):
        if not inspect.isfunction(func):
            raise TypeError('update must be a function')
        if not all([inspect.isfunction(f) for f in after_func]):
            raise TypeError('after_func must be a function')

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
        if not inspect.isfunction(func):
            raise TypeError('update must be a function')

        func.priority = _priority
        return func

    return dec


### utility functions

def set_update_rate(new_ups):
    """sets the update rate to new_ups"""
    global UPS
    UPS = new_ups


def get_update_rate():
    """returns the update rate"""
    return UPS


### run the loop

def run():
    """this is the main run loop"""
    # first we call the setup functions of the modules
    for module in _get('setup'):
        _setup(module)
    try:
        # then we start the update loop
        last_tick = time.time()
        while True:
            # we now tick the update loop
            last_tick = _tick(last_tick)
    except QuitException:
        # if we get a quit exception we trigger the teardown functions of the modules
        for module in _get('teardown'):
            _teardown(module)
        exit()


__all__ = [
    'after',
    'before',
    'priority',
    'set_update_rate',
    'get_update_rate',
    'run',
]