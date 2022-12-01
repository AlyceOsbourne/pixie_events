from .loop import *
from .events import *
from . import raw_input

events.subscribe('quit')


def finish():
    # quit the program
    raise loop.QuitException


@priority(float('inf'))
def __setup__():
    events.register('mouse')
    events.register('keyboard')

    raw_input.setup()


@priority(float('inf'))
def __update__():
    """this is triggered with the highest priority, this will be the main control loop for any subsystems I implement"""
    events.update()
    update_inputs(raw_input.get_input())


def update_inputs(_input):
    events.publish('mouse', **_input['mouse'])
    events.publish('keyboard', _input['keyboard'])


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
