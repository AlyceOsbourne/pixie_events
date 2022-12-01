from types import MappingProxyType

from pynput import keyboard
from pynput import mouse

pressed_keys = {
    k: False for k in keyboard.Key
}

mouse_buttons = {
    b: False for b in mouse.Button
}

mouse_position = {'x': 0, 'y': 0}
scroll = {'x': 0, 'y': 0, 'dx': 0, 'dy': 0}

keyboard_listener = keyboard.Listener(
    on_press=lambda key: pressed_keys.__setitem__(key, True),
    on_release=lambda key: pressed_keys.__setitem__(key, False)
)

mouse_listener = mouse.Listener(
    on_click=lambda x, y, button, pressed: mouse_buttons.__setitem__(button, pressed),
    on_move=lambda x, y: mouse_position.update({'x': x, 'y': y}),
    on_scroll=lambda x, y, dx, dy: scroll.update({'x': x, 'y': y, 'dx': dx, 'dy': dy})
)


def setup():
    print('starting input listener')
    keyboard_listener.daemon = True
    keyboard_listener.start()
    mouse_listener.daemon = True
    mouse_listener.start()


def teardown():
    print('stopping input listener')
    keyboard_listener.stop()
    mouse_listener.stop()


def get_input():
    _input = {
        'keyboard': MappingProxyType(pressed_keys.copy()),
        'mouse': {
            'buttons': MappingProxyType(mouse_buttons.copy()),
            'position': MappingProxyType(mouse_position.copy()),
            'scroll': MappingProxyType(scroll.copy())
        }
    }
    scroll.update({'dx': 0, 'dy': 0})
    return _input




