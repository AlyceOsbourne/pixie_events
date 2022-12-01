from .loop import *
from .events import *
from . import raw_input


def finish():
    # quit the program
    raise loop.QuitException


@priority(float('inf'))
def __setup__():
    # set up system events
    events.subscribe('quit')(finish)
    events.register('mouse')
    events.register('keyboard')
    # trigger input handler
    raw_input.setup()


@priority(float('inf'))
def __update__():
    """this is triggered with the highest priority, this will be the main control loop for any subsystems I implement"""
    for key, value in raw_input.get_input().items():
        events.publish(key, value)
    raw_input.clear_input()
    events.update()


@priority(float('-inf'))
def __teardown__():
    """This is the main program teardown that is called when the program is finished"""
    raw_input.teardown()
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
