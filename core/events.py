from collections import deque
from enum import Flag
from concurrent.futures import ThreadPoolExecutor
events = {}
event_queue = deque()

def subscribe(event):
    def decorator(func):
        events.setdefault(event, []).append(func)
        return func

    return decorator


def publish(event, *args, **kwargs):
    for func in events.get(event, []):
        event_queue.append((func, args, kwargs))


def update():
    curr = event_queue.copy()
    event_queue.clear()
    while curr:
        func, args, kwargs = curr.popleft()
        func(*args, **kwargs)


def teardown():
    events.clear()
    event_queue.clear()


class Event(Flag):
    def subscribe(self, func):
        return subscribe(self)(func)

    def publish(self, *args, **kwargs):
        publish(self, *args, **kwargs)


__all__ = ['Event', 'subscribe', 'publish']
