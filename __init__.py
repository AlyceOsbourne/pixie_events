from src import *
if __name__ == "__main__":
    print("Running this on its own will not do anything, you should import the module and follow the documentation")
else:
    print("Thanks for using Pixie Events")
    __all__ = (
        'loop',
        'run',
        'Event',
        'subscribe',
        'publish',
        'finish',
        'before',
        'after',
        'priority',
    )