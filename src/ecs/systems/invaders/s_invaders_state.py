import esper
import pygame
from src.ecs.components.base import CVelocity, CAnimation, CTransform, CSurface
from src.ecs.components.invaders.c_invader_spawner import CInvaderSpawner
from src.ecs.components.states.c_invader_state import InvaderState, CInvaderState
from src.ecs.components.tags.c_tag_invader import CTagInvader
import pygame


def system_invaders_state(ecs_world: esper.World, screen: pygame.Surface):
    components = ecs_world.get_components(CTransform, CVelocity, CAnimation,
                                          CSurface, CInvaderState, CTagInvader)

    c_transform: CTransform
    c_animation: CAnimation
    c_velocity: CVelocity
    c_invader_state: CInvaderState
    c_invader: CTagInvader
    c_surface: CSurface

    for _, (c_transform, c_velocity, c_animation, c_surface, c_invader_state, c_invader) in components:
        if c_invader_state.state == InvaderState.MOVE:
            _do_move_state(c_velocity, c_animation, c_invader_state, c_invader)
        elif c_invader_state.state == InvaderState.ATTACK:
            _do_attack_state(c_animation, c_invader_state, c_transform, screen, c_surface, c_velocity, c_invader)
        elif c_invader_state.state == InvaderState.RETURN:
            _do_return_state(ecs_world, c_velocity, c_invader_state, c_invader, c_transform, c_surface, c_animation)


def _do_move_state(c_velocity: CVelocity, c_animation: CAnimation,
                   c_invader_state: CInvaderState, c_invader: CTagInvader):
    if c_invader.selected is True:
        c_invader_state.state = InvaderState.ATTACK

        c_invader.selected = False

        c_velocity.vel = c_invader.attack_velocity
        c_velocity.angular_velocity = c_invader.angular_velocity

        if len(c_animation.animations) > 1:
            _set_animation(c_animation, 1)


def _do_attack_state(c_animation: CAnimation, c_invader_state: CInvaderState,
                     c_transform: CTransform, screen: pygame.Surface,
                     c_surface: CSurface, c_velocity: CVelocity, c_invader: CTagInvader):
    if c_transform.pos.y >= (screen.get_height() - c_surface.surf.get_height() - 5):
        c_velocity.vel = c_invader.return_velocity.copy()
        c_velocity.angular_velocity = c_invader.angular_velocity * -1
        c_invader_state.state = InvaderState.RETURN
        c_transform.pos.y = -10
        if len(c_animation.animations) > 1:
            _set_animation(c_animation, 1)


def _do_return_state(ecs_world: esper.World, c_velocity: CVelocity, c_invader_state: CInvaderState, c_invader: CTagInvader,
                     c_transform: CTransform, c_surface: CSurface, c_anim: CAnimation):
    if (abs(c_transform.pos.x - c_invader.oscillation_position.x) > 2.0 or
            abs(c_transform.pos.y - c_invader.oscillation_position.y) > 2.0):
        velocity_normal = _normal_vector_direction(c_invader.oscillation_position, c_transform.pos)
        c_velocity.vel.x = (velocity_normal.x * c_invader.return_velocity.x)
        c_velocity.vel.y = (velocity_normal.y * c_invader.return_velocity.y)
        if c_invader.angle <= 0:
            c_velocity.angular_velocity = 0
    else:
        c_velocity.vel = c_invader.move_velocity.copy()
        c_surface.surf = c_invader.initial_surface
        c_surface.area = c_surface.surf.get_rect()
        c_surface.area.w = c_surface.surf.get_rect().w / c_anim.number_frames
        c_invader_state.state = InvaderState.MOVE
        components = ecs_world.get_component(CInvaderSpawner)
        c_spawner: CInvaderSpawner
        for _, (c_spawner) in components:
            c_spawner.spawn_is_on = False
            c_spawner.time = 0.0


def _set_animation(c_animation: CAnimation, animation_index: int):
    if c_animation.current != animation_index:
        c_animation.current = animation_index
        c_animation.current_time = 0
        c_animation.current_frame = c_animation.animations[c_animation.current].start


def _normal_vector_direction(vector_target: pygame.Vector2, vector_origin: pygame.Vector2) -> pygame.Vector2:
    return (vector_target - vector_origin).normalize()
