from enum import Enum


class ScoreState(Enum):
    ON = 0
    OFF = 1


class CScoreState:
    def __init__(self) -> None:
        self.state = ScoreState.ON