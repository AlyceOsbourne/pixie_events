from _weakrefset import WeakSet
from collections import deque
from enum import Flag

events = {}  # holds event key and callbacks
event_queue = deque()  # event queue


def subscribe(event):
    """Callback decorator for subscribing to events"""

    def decorator(func):
        events.setdefault(event, WeakSet()).add(func)
        return func

    return decorator


def publish(event, *args, **kwargs):
    # publish event to all subscribers
    for func in events.get(event, set()):
        event_queue.append((func, args, kwargs))


def update():
    # processes the events in the queue, probably a more elegant way of doing this?
    curr = event_queue.copy()
    event_queue.clear()
    while curr:
        func, args, kwargs = curr.popleft()
        func(*args, **kwargs)


def teardown():
    # clear the event queue and events
    events.clear()
    event_queue.clear()


class Event(Flag):
    # magical Flag enum that allows for easy creation, subscription and publishing of events
    def subscribe(self, func):
        return subscribe(self)(func)

    def publish(self, *args, **kwargs):
        publish(self, *args, **kwargs)


__all__ = ['Event', 'subscribe', 'publish']
