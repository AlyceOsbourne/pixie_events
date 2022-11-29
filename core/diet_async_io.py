"""A minim AsyncIO implementation using generator coroutines."""
from typing import Generator, Tuple

from . import loop
import time

coroutines: list = []


def update():
    for coroutine in coroutines:
        try:
            coroutine.send(None)
        except StopIteration:
            coroutines.remove(coroutine)


def add(coroutine: Generator):
    """This function assumes you have already primed the coroutine with send(None)."""
    coroutines.append(coroutine)


