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
    from pixie_events import *    # Import the module, utilizes __all__ so is * import safe.

    i = 0   # these are just here to limit how many times this will loop if you run the example
    lim = 3


    class Events(Event):  # Event is a magic Flag enum that allows you to register eny number of Constant events, and subscribe to/emit them
        ping = 1


    @Events.ping.subscribe  # Example of subscribing to events
    def pong():
        print('Pong')


    def setup():  # called when run is first called accross all module that import pixie events and has this function
        print('Setting up...')


    @before(lambda: print('Before'))  # can be used to run a function before the update loop (or technically any other function)
    @after(lambda: print('After'))  # ditto, but after the function
    def update():
        global i
        print('Ping')
        Events.ping.publish()  # publish events like this, you can pass args and kwargs to this and it will call all callbacks with those args
        if i == lim:
            finish()  # call finish to end the program
        i += 1


    def teardown():  # is called when finish has been called (raises an exit exception behind the scenes)
        print('Tearing Down...')

    run()  # this runs the program loop
```