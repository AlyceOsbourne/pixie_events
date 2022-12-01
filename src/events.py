from _weakrefset import WeakSet
from collections import deque
from enum import Flag


_events = {}  # holds event key and callbacks
_event_queue = deque()  # event queue


def register(name):
    """Registers an event with the given name"""
    return _events.setdefault(name, WeakSet())


def subscribe(event):
    """Callback decorator for subscribing to events"""

    def decorator(func):
        register(event).add(func)
        return func
    return decorator


def publish(event, *args, **kwargs):
    # publish event to all subscribers
    if event not in _events:
        raise ValueError(f'Event {event} has no subscribers')
    for func in _events.get(event):
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


class EventAttr:
    # this is an observable attribute descriptor essentially that fires an event when the attribute is set
    def __init__(self, event_name):
        self.event_name = event_name
        register(event_name)

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        publish(self.event_name, instance, value)


class Event(Flag):
    # magical Flag enum that allows for easy creation, subscription and publishing of events
    def subscribe(self, func):
        return subscribe(self.name)(func)

    def publish(self, *args, **kwargs):
        publish(self.name, *args, **kwargs)


__all__ = ['Event', 'subscribe', 'publish', 'register', 'EventAttr']
