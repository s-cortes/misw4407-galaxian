from pygame import Vector2


class CTagIntro:
    def __init__(self, pos_fin: Vector2) -> None:
        self.pos_fin = pos_fin
        self.minimum_distance = 2
        self.moving = True
