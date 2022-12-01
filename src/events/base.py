from _weakrefset import WeakSet
from collections import deque

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


def _update():
    # processes the events in the queue, probably a more elegant way of doing this?
    curr = _event_queue.copy()
    _event_queue.clear()
    while curr:
        func, args, kwargs = curr.popleft()
        func(*args, **kwargs)


def _teardown():
    # clear the event queue and events
    _events.clear()
    _event_queue.clear()


__all__ = ['subscribe', 'publish', 'register', '_teardown', '_update']