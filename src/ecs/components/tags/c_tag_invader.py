import pygame
from pygame import Surface


class CTagInvader:
    def __init__(self, start_position: pygame.Vector2, attack_velocity: pygame.Vector2,
                 angular_velocity: float, return_velocity: pygame.Vector2,
                 move_velocity: pygame.Vector2, initial_surface: Surface, single_surface: Surface,
                 launch_sound: str, invader_points: int) -> None:
        self.start_position = start_position
        self.oscillation_position = start_position.copy()
        self.attack_velocity = attack_velocity
        self.return_velocity = return_velocity
        self.move_velocity = move_velocity
        self.angular_velocity = angular_velocity
        self.angle = 0
        self.selected = False
        self.initial_surface = initial_surface
        self.single_surface = single_surface
        self.launch_sound = launch_sound
        self.invader_points = invader_points
