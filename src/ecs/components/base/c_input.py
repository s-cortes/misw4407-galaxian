from enum import Enum


class InputPhase(Enum):
    NA = 0
    START = 1
    END = 2


class CInput:
    def __init__(self, name: str, key: int) -> None:
        self.name = name
        self.key = key
        self.phase = InputPhase.NA
