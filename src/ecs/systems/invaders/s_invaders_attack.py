from esper import World
from src.ecs.components.base import CTransform, CVelocity, CSurface
from src.ecs.components.states.c_invader_state import CInvaderState, InvaderState
from src.ecs.components.tags.c_tag_invader import CTagInvader
from pygame import Vector2
import pygame


def system_invaders_attack(world: World, player_entity: int, delta_time: float):
    if player_entity is None:
        return

    components = world.get_components(CVelocity, CTransform, CSurface, CInvaderState, CTagInvader)
    c_player_transform = world.component_for_entity(player_entity, CTransform)
    c_velocity: CVelocity
    c_transform: CTransform
    c_invader: CTagInvader
    c_surface: CSurface
    c_invader_state: CInvaderState

    for _, (c_velocity, c_transform, c_surface, c_invader_state, c_invader) in components:
        if c_invader_state.state == InvaderState.ATTACK:
            if c_invader.angle >= 180:
                c_velocity.angular_velocity = 0.0

            target_vector: Vector2

            if c_transform.pos.distance_to(c_player_transform.pos) > 50:
                target_vector = c_player_transform.pos - c_transform.pos
            else:
                outbound_target = c_transform.pos.copy()
                outbound_target.y = 4000
                target_vector = outbound_target - c_transform.pos
            target_vector.normalize_ip()
            target_vector.scale_to_length(c_velocity.vel.magnitude())
            direction_vector = target_vector - c_velocity.vel
            final_vector = c_velocity.vel + direction_vector
            c_velocity.vel = final_vector.lerp(final_vector, (5 * delta_time))


def _normal_vector_direction(vector_target: pygame.Vector2, vector_origin: pygame.Vector2) -> pygame.Vector2:
    return (vector_target - vector_origin).normalize()