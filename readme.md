## Pixie Events
___
This system includes a core program loop, and global functions that are automatically called if the module is imported

### The Global Functions

`setup()`
is called automatically on run, can be used to initialize variables and program states

`update()`
is called automatically every frame

`teardown()`
is called on program close, can be used to save data

### Example:

```python
    from pixie_events import *

    i = 0
    lim = 0

    # everything here is run dynamically, just run the core and it will find and run these functions
    # across all modules (provided they are imported, I recommend a run module for this)

    class Events(Event):  # create events easily
        ping = 1
        quit = 2


    @Events.ping.subscribe  # subscribe to events
    def pong():
        print('Pong')


    def setup():  # set up function, called on run
        print('Setting up...')
        Events.quit.subscribe(finish)


    @before(lambda: print('Before'))  # decorator to add functions to be ran before the update function
    @after(lambda: print('After'))  # decorator to add functions to be ran after the update function
    @priority(1)  # control flow using priority
    def update(
    ):
        global i
        print('Ping')
        Events.ping.publish()  # publish events
        if i == lim:
            Events.quit.publish()
        i += 1


    def teardown():  # tear down function, called on finish
        print('Tearing Down...\a\b')


    run()  # run the core
```