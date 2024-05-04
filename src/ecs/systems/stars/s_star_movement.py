from esper import World
from src.ecs.components.base import CTransform, CVelocity
from src.ecs.components.tags import CTagStar


def system_star_movement(world: World, delta_time: int):
    components = world.get_components(CVelocity, CTransform, CTagStar)

    c_velocity: CVelocity
    c_transform: CTransform
    for _, (c_velocity, c_transform, _) in components:
        c_transform.pos.x += c_velocity.vel.x * delta_time
        c_transform.pos.y += c_velocity.vel.y * delta_time
