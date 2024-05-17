from enum import Enum


class LevelState(Enum):
    GAME_INTRO = 0
    GAME_STARTED = 1
    LEVEL_STARTED = 2
    LEVEL_WON = 3
    LEVEL_LOST = 4
    GAME_WON = 5
    GAME_LOST = 6


class CLevelState:
    def __init__(self):
        self.state = LevelState.GAME_INTRO
