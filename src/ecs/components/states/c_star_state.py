from enum import Enum

from pygame import Color, Vector2


class StarState(Enum):
    HIDE = 0
    SHOW = 1


class CStarState:
    def __init__(self, show_color: Color, hide_color: Color):
        self.state = StarState.SHOW
        self.colors: tuple[Color] = (hide_color, show_color)
