from _weakrefset import WeakSet

to_update = WeakSet()


class UpdatableMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if hasattr(cls, '__update_class__'):
            to_update.add(getattr(cls, '__update_class__'))
        return cls


class Updatable(metaclass=UpdatableMeta):
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        setattr(self, '__instances__', WeakSet())
        return self

    @classmethod
    def __update_class__(cls):
        for instance in getattr(cls, '__instances__'):
            getattr(instance, '__update__')()


def update():
    for _update in to_update:
        _update()


__all__ = ('UpdatableMeta', 'Updatable')