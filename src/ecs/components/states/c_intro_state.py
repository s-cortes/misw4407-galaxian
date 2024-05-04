from enum import Enum

from pygame import Vector2


class IntroState(Enum):
    IDLE = 0
    LOADING = 1


class CIntroState:
    def __init__(self):
        self.state = IntroState.LOADING
