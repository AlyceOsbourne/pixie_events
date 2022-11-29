from core import *
import test_update

if __name__ == "__main__":

    i = 0
    lim = 3


    class Events(Event):
        ping = 1

    @Events.ping.subscribe
    def pong():
        print('Pong')


    def setup():
        print('Setting up...')


    @before(lambda: print('Before'))
    @after(lambda: print('After'))
    def update(priority = 1): # control the order of the update functions by adding the priority keyword argument
        global i
        print('Ping')
        Events.ping.publish()
        if i == lim:
            finish()
        i += 1


    def teardown():
        print('Tearing Down...')

    run()
else:
    print("Thanks for using Pixie Events")
