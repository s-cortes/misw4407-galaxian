from esper import World
from src.ecs.components.base import CTransform, CVelocity, CSurface, CAnimation
from src.ecs.components.states.c_invader_state import CInvaderState, InvaderState
from src.ecs.components.tags.c_tag_invader import CTagInvader
import pygame


def system_invaders_movement(world: World, level_cfg: dict, delta_time: float):
    components = world.get_components(CVelocity, CTransform, CSurface, CAnimation, CInvaderState,  CTagInvader)

    c_velocity: CVelocity
    c_transform: CTransform
    c_invader: CTagInvader
    c_surface: CSurface
    c_invader_state: CInvaderState

    for _, (c_velocity, c_transform, c_surface, c_anim, c_invader_state, c_invader) in components:
        c_transform.pos.x += c_velocity.vel.x * delta_time
        c_transform.pos.y += c_velocity.vel.y * delta_time
        c_invader.start_position.x += c_velocity.vel.x * delta_time

        if c_invader_state.state != InvaderState.MOVE:
            c_invader.angle += c_velocity.angular_velocity
            c_surface.surf = pygame.transform.rotate(c_invader.single_surface.copy(), c_invader.angle)
            c_surface.area = c_surface.surf.get_rect()



