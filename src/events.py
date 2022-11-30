from _weakrefset import WeakSet
from collections import deque
from enum import Flag
from itertools import count

_events = {}  # holds event key and callbacks
_event_queue = deque()  # event queue
_event_id = count()


def subscribe(event):
    """Callback decorator for subscribing to events"""

    def decorator(func):
        _events.setdefault(event, WeakSet()).add(func)
        return func

    return decorator


def publish(event, *args, **kwargs):
    # publish event to all subscribers
    for func in _events.get(event, set()):
        _event_queue.append((func, args, kwargs))


def update():
    # processes the events in the queue, probably a more elegant way of doing this?
    curr = _event_queue.copy()
    _event_queue.clear()
    while curr:
        func, args, kwargs = curr.popleft()
        func(*args, **kwargs)


def teardown():
    # clear the event queue and events
    _events.clear()
    _event_queue.clear()


class Event(Flag):
    # magical Flag enum that allows for easy creation, subscription and publishing of events
    def subscribe(self, func):
        return subscribe(self)(func)

    def publish(self, *args, **kwargs):
        publish(self, *args, **kwargs)

    def __new__(cls, *args, **kwargs):
        cls._value_ = next(_event_id)
        return cls

    @staticmethod
    def event(name):
        # searches all subclass members for an event with the same name,
        # this allows you to register events anywhere, and access them though the class
        # this should be done in the setup function of the module
        for sub_cls in Event.__class__.__subclasses__():
            for member in sub_cls.__members__.values():
                if member.name == name:
                    return member
        raise AttributeError(f'Event {name} not found')


__all__ = ['Event', 'subscribe', 'publish']
