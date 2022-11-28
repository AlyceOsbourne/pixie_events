"""import this module and it will apply a fps lock to your game"""
from . import loop
import time

fps = 1
last_time = time.time()
delta_time = 0
lock = True


def update():
    global last_time, delta_time
    print('updating fps')
    if lock:
        print('locking')
        sleep_time = 1 / fps - (time.time() - last_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
    delta_time = time.time() - last_time
    last_time = time.time()
    print(f"deltatime: {delta_time}")


def set_fps(new_fps):
    global fps
    fps = new_fps


def get_fps():
    return fps


def get_delta_time():
    return delta_time


def set_lock(new_lock):
    global lock
    lock = new_lock
