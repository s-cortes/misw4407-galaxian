from pygame import Surface

from esper import World
from src.ecs.components.base import CSurface, CTransform, CVelocity
from src.ecs.components.tags import CTagStar


def system_star_screen_bounce(world: World, screen: Surface):
    components = world.get_components(CTransform, CSurface, CTagStar)
    screen_rect = screen.get_rect()

    c_transform: CTransform
    c_surface: CSurface
    for _, (c_transform, c_surface, _) in components:
        cuad_rect = CSurface.get_relative_area(c_surface.area, c_transform.pos)

        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            c_transform.pos.y = 0

