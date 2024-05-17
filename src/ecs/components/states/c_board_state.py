from enum import Enum


class BoardState(Enum):
    IDLE = 0
    LOADING = 1


class CBoardState:
    def __init__(self):
        self.state = BoardState.LOADING
