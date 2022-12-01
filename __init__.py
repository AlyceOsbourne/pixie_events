from src import *

if __name__ == "__main__":

    e, i, m = None, 0, 100


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

    def teardown():
        print('teardown')

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
