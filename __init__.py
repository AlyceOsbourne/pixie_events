from core import *

if __name__ == "__main__":

    i = 0
    lim = 1
    # everything here is ran dynamically, just run the core and it will find and run these functions
    # across all modules (provided they are imported, I recommend a run module for this)

    class Events(Event):  # create events easily
        ping = 1

    @Events.ping.subscribe  # subscribe to events
    def pong():
        print('Pong')


    def setup():  # set up function, called on run
        print('Setting up...')


    @before(lambda: print('Before'))  # decorator to add functions to be ran before the update function
    @after(lambda: print('After'))  # decorator to add functions to be ran after the update function
    @priority(1)  # control flow using priority
    def update(
    ):
        global i
        print('Ping')
        Events.ping.publish()  # publish events
        if i == lim:
            finish()
        i += 1


    def teardown():  # tear down function, called on finish
        print('Tearing Down...')

    run()  # run the core
else:
    print("Thanks for using Pixie Events")
