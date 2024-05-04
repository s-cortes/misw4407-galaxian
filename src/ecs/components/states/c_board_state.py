from enum import Enum

from pygame import Vector2


class BoardState(Enum):
    IDLE = 0
    LOADING = 1


class CBoardState:
    def __init__(self):
        self.state = BoardState.LOADING
