import sys
import inspect
from functools import cache


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


def _get():
    yield from (
        module for module
        in list(sys.modules.values()) if
        _predicate(module)
    )


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
        return wrapper
    return dec


def after(*after_func):
    def dec(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for _func in after_func:
                _func()
            return result
        return wrapper
    return dec


def run():
    for module in _get():
        _setup(module)
    try:
        while True:
            for module in _get():
                _update(module)
    except QuitException:
        for module in _get():
            _teardown(module)
        exit()