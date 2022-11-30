from src import *

if __name__ == "__main__":
    # give example of the global system in action

    e, i, m = None, 0, 100
    set_update_rate(1)

    class TestAttribute:
        event_attr = EventAttr('test')


    def setup():
        subscribe('test')(print)
        global e
        e = TestAttribute()


    def update():
        global i
        e.event_attr = (i := i + 1)
        if i >= m:
            finish()

    run()


else:
    print("Thanks for using Pixie Events")
    __all__ = (
        'loop',
        'run',
        'register',
        'subscribe',
        'publish',
        'finish',
        'before',
        'after',
        'priority',
    )
