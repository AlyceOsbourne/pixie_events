from .loop import *
from .events import *
from . import raw_input

def finish():
    # quit the program
    raise loop.QuitException


# these functions are automatically called by the loop, no need to add them manually
# they do not become available globally, but they are ran by a global loop

@priority(float('inf'))
def setup():
    events.subscribe('quit')(finish)
    events.register('mouse')
    events.register('keyboard')
    events.subscribe('mouse')(print)
    events.subscribe('mouse')(print)



@priority(float('inf'))
def update():
    """this is triggered with the highest priority, this will be the main control loop for any subsystems I implement"""
    for key, value in raw_input.get_input().items():
        events.publish(key, value)
    events.update()


@priority(float('-inf'))
def teardown():
    """This is the main program teardown that is called when the program is finished"""
    events.teardown()


__all__ = [
    'after',
    'before',
    'Event',
    'EventAttr',
    'finish',
    'get_update_rate',
    'loop',
    'priority',
    'publish',
    'register',
    'run',
    'set_update_rate',
    'subscribe',
]
