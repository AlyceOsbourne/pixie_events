from src import subscribe, publish, finish, run, register, before, after, priority, EventAttr

if __name__ == "__main__":
    import time


    class ItsMagic:
        observed_attr = EventAttr('on_attr_change')

        def __init__(self):
            self.observed_attr = 0


    magic = ItsMagic()


    @subscribe('on_attr_change')
    def on_attr_changed(instance, value):
        print('observed_attr changed to ', value, ' on ', instance)
        if value == 500:
            finish()


    @subscribe('message')
    def m(msg):
        print(msg)


    @subscribe('mouse')
    def mouse(buttons, position, scroll):
        print({
                  button for button, pressed in buttons.items() if pressed
              } or "No Buttons Pressed", position, scroll)


    @subscribe('keyboard')
    def keyboard(keys):
        print({key for key, value in keys.items() if value} or 'no keys pressed')


    def __setup__():
        register('message')


    def __update__():
        magic.observed_attr += 1
        publish('message', time.strftime('%H:%M:%S:%p'))


    def __teardown__():
        publish('message', 'done')


    run()

else:
    __all__ = (
        'run',
        'register',
        'subscribe',
        'publish',
        'finish',
        'before',
        'after',
        'priority',
    )
