"""If you have imported this module directly, you are probably doing something funky"""

import inspect
import sys
import time
from functools import cache

UPS = 60  # updates per second


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
        not any([inspect.isfunction(getattr(module, attr, None)) for attr in ('setup', 'update', 'teardown')]),
    ))


@cache
def _sort_key(module, f_name):
    """Checks the module for the function name and returns the priority if it exists on the function object,
    otherwise returns 0 """
    if (
            not hasattr(module, f_name)
            or not hasattr(getattr(module, f_name), 'priority')
    ):
        return 0
    return getattr(getattr(module, f_name), 'priority')


@cache
def _sort(modules, f_name):
    """sorts the modules by the priority of the update function"""
    return sorted(modules, key=lambda m: _sort_key(m, f_name), reverse=True)


def _get(f_name):
    """gets the modules for the project, sorted by priority"""
    yield from _sort((
        module for module
        in set(sys.modules.values()) if
        _predicate(module)
    ), f_name)


### magic function callers

def _setup(module):
    """calls the setup function of the module if it exists"""
    if hasattr(module, 'setup'):
        if inspect.isfunction(module.setup):
            return module.setup()
        print(f'WARNING: {module.__name__}.setup is not a function')


def _update(module):
    """calls the update function of the module if it exists"""
    if hasattr(module, 'update'):
        if inspect.isfunction(module.update):
            return module.update()
        print(f'WARNING: {module.__name__}.update is not a function')


def _teardown(module):
    """calls the teardown function of the module if it exists"""
    if hasattr(module, 'teardown'):
        if inspect.isfunction(module.teardown):
            return module.teardown()
        print(f'WARNING: {module.__name__}.teardown is not a function')


def _tick(last_tick):
    """update tick, updates all the update function and then returns limits the update rate"""
    for module in _get('update'):
        _update(module)
    return _lim(last_tick)
