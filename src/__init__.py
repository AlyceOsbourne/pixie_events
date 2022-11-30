from .loop import *
from .events import *


class SystemEvents(Event):
    Quit = """These values don't actually matter, you are just declaring a constant for events, the value you input 
    here are completely disregarded, I will come up with a more elegant way to do this, I may make a register events
    method that is called, that dynamically creates this little event system with the easy decos"""


def finish():
    # quit the program
    raise loop.QuitException


# these functions are automatically called by the loop, no need to add them manually
# they do not become available globally, but they are ran by a global loop

@priority(float('inf'))
def setup():
    """For now, we have no setup required at this level, but keeping it here to show implementation details"""
    SystemEvents.Quit.subscribe(finish)


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
