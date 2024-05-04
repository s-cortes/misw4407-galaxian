from pygame import Color, Surface, Vector2

from esper import World
from src.ecs.components.base import CAnimation, CSurface, CTransform, CVelocity


def create_square(
    world: World, pos: Vector2, size: Vector2, vel: Vector2, color: Color
) -> int:
    entity = world.create_entity()
    world.add_component(entity, CSurface(size, color))
    world.add_component(entity, CTransform(pos))
    world.add_component(entity, CVelocity(vel))
    return entity


def create_sprite(
    world: World,
    pos: Vector2,
    surface: Surface,
    vel: Vector2,
    c_anim: CAnimation = None,
) -> int:
    entity = world.create_entity()
    world.add_component(entity, CTransform(pos))
    world.add_component(entity, CVelocity(vel))

    c_surface = CSurface.from_surface(surface)
    if c_anim:
        rect_surf = c_surface.surf.get_rect()
        c_surface.area.w = rect_surf.w / c_anim.number_frames
        c_surface.area.x = c_surface.area.w * c_anim.current_frame
    world.add_component(entity, c_surface)

    return entity


def get_color(config: dict, key: str = None):
    r = config[key]["r"] if key else config["r"]
    g = config[key]["g"] if key else config["g"]
    b = config[key]["b"] if key else config["b"]
    return (r, g, b)
