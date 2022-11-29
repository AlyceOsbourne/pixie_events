from . import loop, diet_async_io
from .events import publish, subscribe, Event

before = loop.before
after = loop.after
run = loop.run
add_coroutine = diet_async_io.add


def finish():
    raise loop.QuitException


def update():
    events.update()


def teardown():
    events.teardown()


__all__ = ['loop', 'run', 'Event', 'subscribe', 'publish', 'finish', 'before', 'after', 'add_coroutine']
