from enum import Enum


class InvaderState(Enum):
    MOVE = 1
    ATTACK = 2
    RETURN = 3


class CInvaderState:
    def __init__(self) -> None:
        self.state = InvaderState.MOVE
