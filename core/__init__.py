from .loop import *
from .events import *


def finish():
    raise loop.QuitException


@priority(float('-inf'))
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
    'priority',
]
