
"""If you have imported this module directly, you are probably doing something funky"""

import inspect
import sys
import time
from functools import cache, wraps

UPS = 60  # updates per second


class QuitException(KeyboardInterrupt):
    """is called to break the update loop"""


def _lim(last_time):
    """limits the update rate to UPS"""
    sleep_time = 1 / UPS - (time.time() - last_time)
    if sleep_time > 0:
        time.sleep(sleep_time)
    last_time = time.time()
    return last_time


### collect modules

@cache
def _predicate(module):
    """Check to see if the module is part of the current project and not a builtin or third party module,
    and checks it has any of the magic methods, cached, so we only ever need to run once per module"""
    return not any((
        module is None,
        not inspect.ismodule(module),
        module is sys.modules[__name__],
        not hasattr(module, '__file__'),
        not getattr(module, '__file__', '').startswith(sys.path[0]),
        not any(
            [inspect.isfunction(getattr(module, attr, None)) for attr in ('__setup__', '__update__', '__teardown__')]),
    ))


@cache
def _sort_key(module, f_name):
    """Checks the module for the function name and returns the priority if it exists on the function object,
    otherwise returns almost minus infinity, this is so you can have a range of values, and make it so that any
    defined priority takes precedence """
    if (
            not hasattr(module, f_name)
            or not hasattr(getattr(module, f_name), 'priority')
    ):
        return float('-inf') + 10
    return getattr(getattr(module, f_name), 'priority')


@cache
def _sort(modules, f_name):
    """sorts the modules by the priority of the update function"""
    return sorted(modules, key=lambda m: _sort_key(m, f_name), reverse=True)


def get(f_name):
    """gets the modules for the project, sorted by priority"""
    yield from _sort((
        module for module
        in set(sys.modules.values()) if
        _predicate(module)
    ), f_name)


### magic function callers

def setup(module):
    """calls the setup function of the module if it exists"""
    if hasattr(module, '__setup__'):
        if inspect.isfunction(module.__setup__):
            return module.__setup__()
        print(f'WARNING: {module.__name__}.setup is not a function')


def update(module):
    """calls the update function of the module if it exists"""
    if hasattr(module, '__update__'):
        if inspect.isfunction(module.__update__):
            return module.__update__()
        print(f'WARNING: {module.__name__}.update is not a function')


def teardown(module):
    """calls the teardown function of the module if it exists"""
    if hasattr(module, '__teardown__'):
        if inspect.isfunction(module.__teardown__):
            return module.__teardown__()
        print(f'WARNING: {module.__name__}.teardown is not a function')


def tick(last_tick):
    """update tick, updates all the update function and then returns limits the update rate"""
    for module in get('__update__'):
        update(module)
    return _lim(last_tick)


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
    global UPS
    UPS = new_ups


def get_update_rate():
    """returns the update rate"""
    return UPS


### run the loop

def run():
    """this is the main run loop"""
    for module in get('setup'):
        setup(module)
    try:
        last_tick = time.time()
        while True:
            last_tick = tick(last_tick)
    except KeyboardInterrupt:
        _exit()
    except Exception as e:
        print(e)
        _exit()


def _exit():
    for module in get('teardown'):
        teardown(module)
    exit()


__all__ = [
    'after',
    'before',
    'priority',
    'set_update_rate',
    'get_update_rate',
    'run',
]
