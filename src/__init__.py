from .loop import *
from .events import *


def finish():
    # quit the program
    raise loop.QuitException


# these functions are automatically called by the loop, no need to add them manually
# they do not become available globally, but they are ran by a global loop

@priority(float('inf'))
def setup():
    subscribe('quit')(finish)


@priority(float('inf'))
def update():
    """this is triggered with the highest priority, this will be the main control loop for any subsystems I implement"""
    events.update()


@priority(float('-inf'))
def teardown():
    """This is the main program teardown that is called when the program is finished"""
    events.teardown()


__all__ = [
    'loop',
    'run',
    'subscribe',
    'publish',
    'finish',
    'before',
    'after',
    'priority',
    'register',
    'Event',
    'EventAttr',
    'set_update_rate',
    'get_update_rate',
]
