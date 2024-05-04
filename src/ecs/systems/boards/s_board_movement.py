from esper import World
from src.ecs.components.base import CTransform, CVelocity
from src.ecs.components.tags import CTagBoard
from src.ecs.components.states import CBoardState


def system_board_movement(world: World, delta_time: int):
    components = world.get_components(CVelocity, CTransform, CBoardState, CTagBoard)

    c_velocity: CVelocity
    c_transform: CTransform
    c_state: CBoardState
    for _, (c_velocity, c_transform, c_state, _) in components:
        c_transform.pos.x += c_state.state.value * c_velocity.vel.x * delta_time
        c_transform.pos.y += c_state.state.value * c_velocity.vel.y * delta_time
