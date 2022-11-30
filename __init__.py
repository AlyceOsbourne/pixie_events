from core import before, Event, finish, run, after, priority

if __name__ == "__main__":

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
else:
    print("Thanks for using Pixie Events")
