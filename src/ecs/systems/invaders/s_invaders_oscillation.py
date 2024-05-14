from esper import World
from src.ecs.components.base import CTransform, CVelocity
from src.ecs.components.states.c_invader_state import CInvaderState, InvaderState
from src.ecs.components.tags.c_tag_invader import CTagInvader


def system_invaders_oscillation(world: World, level_cfg: dict, delta_time: float):
    components = world.get_components(CVelocity, CTransform, CInvaderState, CTagInvader)

    c_velocity: CVelocity
    c_transform: CTransform
    c_invader_state: CInvaderState
    c_invader: CTagInvader

    for _, (c_velocity, c_transform, c_invader_state,  c_invader) in components:
        if c_invader_state.state == InvaderState.MOVE:
            if c_velocity.vel.x == 0:
                c_velocity.vel.x = c_invader.move_velocity.x
            if abs(c_invader.start_position.x - c_transform.pos.x) >= level_cfg['invaders_range']:
                c_velocity.vel.x *= -1
                c_invader.move_velocity.x *= -1


        else:
            if abs(c_invader.start_position.x - c_invader.oscillation_position.x) >= level_cfg['invaders_range']:
                c_invader.move_velocity.x *= -1

