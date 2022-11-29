import sys
import inspect
import time
from functools import cache, wraps

UPS = 60


class QuitException(Exception):
    pass


@cache
def _predicate(module):
    return not any((
        module is None,
        not inspect.ismodule(module),
        module is sys.modules[__name__],
        not hasattr(module, '__file__'),
        not getattr(module, '__file__', '').startswith(sys.path[0]))
    )


@cache
def _sort_key(module):
    if hasattr(module, 'update'):
        if inspect.isfunction(module.update):
            sig = inspect.signature(module.update)
            if 'priority' in sig.parameters:
                return sig.parameters['priority'].default
    return 0


@cache
def _sort(modules):
    return sorted(modules, key=_sort_key, reverse=True)


def _get():
    yield from _sort((
        module for module
        in list(sys.modules.values()) if
        _predicate(module)
    ))


def _setup(module):
    if hasattr(module, 'setup'):
        if inspect.isfunction(module.setup):
            return module.setup()
        print(f'WARNING: {module.__name__}.setup is not a function')


def _teardown(module):
    if hasattr(module, 'teardown'):
        if inspect.isfunction(module.teardown):
            return module.teardown()
        print(f'WARNING: {module.__name__}.teardown is not a function')


def _lim(last_time):
    sleep_time = 1 / UPS - (time.time() - last_time)
    if sleep_time > 0:
        time.sleep(sleep_time)
    last_time = time.time()
    return last_time


def _update(module):
    if hasattr(module, 'update'):
        if inspect.isfunction(module.update):
            return module.update()
        print(f'WARNING: {module.__name__}.update is not a function')


def before(*before_func):
    def dec(func):
        def wrapper(*args, **kwargs):
            for _func in before_func:
                _func()
            return func(*args, **kwargs)

        return wraps(func)(wrapper)

    return dec


def after(*after_func):
    def dec(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for _func in after_func:
                _func()
            return result

        return wraps(func)(wrapper)

    return dec


def update_rate(new_fps):
    global UPS
    UPS = new_fps


def get_update_rate():
    return UPS


def run():
    last_time = time.time()
    for module in _get():
        _setup(module)
    try:
        while True:
            for module in _get():
                _update(module)
            last_time = _lim(last_time)
    except QuitException:
        for module in _get():
            _teardown(module)
        exit()
