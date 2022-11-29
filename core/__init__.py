from . import loop
from .events import publish, subscribe, Event

before = loop.before
after = loop.after
run = loop.run
priority = loop.priority

def finish():
    raise loop.QuitException


def update():
    events.update()


def teardown():
    events.teardown()


__all__ = [
    'loop',
    'run',
    'Event',
    'subscribe',
    'publish',
    'finish',
    'before',
    'after',
    'priority'
]
