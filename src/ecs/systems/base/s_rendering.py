from pygame import Surface

from esper import World
from src.ecs.components.base import CSurface, CTransform


def system_rendering(world: World, screen: Surface):
    components = world.get_components(CTransform, CSurface)

    c_transform: CTransform
    c_surface: CSurface
    for _, (c_transform, c_surface) in components:
        screen.blit(c_surface.surf, c_transform.pos, area=c_surface.area)
