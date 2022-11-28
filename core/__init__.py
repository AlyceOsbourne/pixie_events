from . import loop
from .events import *

before = loop.before
after = loop.after
run = loop.run


def finish():
    raise loop.QuitException


def update():
    events.update()


def teardown():
    events.teardown()


__all__ = ['loop', 'run', 'Event', 'subscribe', 'publish', 'finish', 'before', 'after']
