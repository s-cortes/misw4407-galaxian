from enum import Enum


class InputName(Enum):
    PLAYER_P = "PLAYER_P"
    PLAYER_Z = "PLAYER_Z"
    PLAYER_RIGHT = "PLAYER_RIGHT"
    PLAYER_LEFT = "PLAYER_LEFT"
    PLAYER_SPACE = "PLAYER_SPACE"
class InputPhase(Enum):
    NA = 0
    START = 1
    END = 2


class CInput:
    def __init__(self, name: InputName, key: int) -> None:
        self.name: InputName = name
        self.key: int = key
        self.phase = InputPhase.NA
