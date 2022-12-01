from types import MappingProxyType

from pynput import keyboard
from pynput import mouse


pressed_keys = set()
mouse_buttons = set()
mouse_position = {'x': 0, 'y': 0}
scroll = {'x': 0, 'y': 0, 'dx': 0, 'dy': 0}

on_press = lambda key: pressed_keys.add(key)
on_release = lambda key: pressed_keys.remove(key)
on_click = lambda x, y, button, pressed: mouse_buttons.add(button) if pressed else mouse_buttons.remove(button)
on_move = lambda x, y: mouse_position.update({'x': x, 'y': y})
on_scroll = lambda x, y, dx, dy: scroll.update({'x': x, 'y': y, 'dx': dx, 'dy': dy})

keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)


def _setup():
    print('Starting input listeners')
    keyboard_listener.start()
    mouse_listener.start()


def _teardown():
    print('Stopping input listeners')
    keyboard_listener.stop()
    mouse_listener.stop()


def get_input():
    return {
        'keyboard': frozenset(pressed_keys),
        'mouse': {
            'buttons': frozenset(mouse_buttons),
            'position': MappingProxyType(mouse_position),
            'scroll': frozenset(scroll),
        }
    }


