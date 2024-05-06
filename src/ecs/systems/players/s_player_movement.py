from esper import World
from src.ecs.components.base import CTransform, CVelocity
from src.ecs.components.tags import CTagPlayer


def system_player_movement(world: World, delta_time: int, pause: bool):
    if pause:
        return
    components = world.get_components(CVelocity, CTransform, CTagPlayer)

    c_velocity: CVelocity
    c_transform: CTransform
    c_player: CTagPlayer
    for _, (c_velocity, c_transform, c_player) in components:

        v_x, v_y = 0, 0
        if c_player.left:
            v_x -= c_velocity.vel.x
        if c_player.right:
            v_x += c_velocity.vel.x

        c_transform.pos.x += v_x * delta_time
        c_transform.pos.y += v_y * delta_time
