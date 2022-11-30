from .loop import *
from .events import *


def finish():
    # quit the program
    raise loop.QuitException


# these functions are automatically called by the loop, no need to add them manually
# they do not become available globally, but they are ran by a global loop

@priority(float('inf'))
def setup():
    """For now, we have no setup required at this level, but keeping it here to show implementation details"""
    # this is where I may wish to set up system event handlers etc


@priority(float('inf'))
def update():
    """this is triggered with the highest priority, this will be the main control loop for any subsystems I implement"""
    events.update()


@priority(float('-inf'))
def teardown():
    """This is the main program teardown that is called when the program is finished"""
    events.teardown()
    # this could be used for data serialization on program exit, amongst other things


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
