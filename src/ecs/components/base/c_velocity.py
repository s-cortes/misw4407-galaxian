from pygame import Vector2


class CVelocity:
    def __init__(self, vel: Vector2) -> None:
        self.vel: Vector2 = vel
        self.angular_velocity = 0.0
