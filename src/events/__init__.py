from enum import Flag

from .base import subscribe, publish, register, update, teardown


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
        publish(self.event_name, value)


class Event(Flag):
    # magical Flag enum that allows for easy creation, subscription and publishing of events
    def subscribe(self, func):
        return subscribe(self.name)(func)

    def publish(self, *args, **kwargs):
        publish(self.name, *args, **kwargs)


__all__ = ['Event', 'subscribe', 'publish', 'register', 'EventAttr']
