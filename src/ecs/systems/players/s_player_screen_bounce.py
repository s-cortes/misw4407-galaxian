from pygame import Surface

from esper import World
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.tags import CTagPlayer


def system_player_screen_bounce(world: World, screen: Surface):
    components = world.get_components(CTransform, CSurface, CTagPlayer)
    screen_rect = screen.get_rect()

    c_transform: CTransform
    c_surface: CSurface
    for _, (c_transform, c_surface, _) in components:
        cuad_rect = CSurface.get_relative_area(c_surface.area, c_transform.pos)
        if any([cuad_rect.left < 0, cuad_rect.right > screen_rect.width]):
            cuad_rect.clamp_ip(screen_rect)
            c_transform.pos.x = cuad_rect.x
            c_transform.pos.y = cuad_rect.y
