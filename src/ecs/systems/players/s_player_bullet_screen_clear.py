from pygame import Surface

from esper import World
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.tags import CTagPlayer, CTagPlayerBullet


def system_player_bullet_screen_clear(world: World, player_tag: CTagPlayer):
    components = world.get_components(CTransform, CSurface, CTagPlayerBullet)

    c_transform: CTransform
    c_surface: CSurface
    for bullet_entity, (c_transform, c_surface, _) in components:
        cuad_rect = CSurface.get_relative_area(c_surface.area, c_transform.pos)
        if cuad_rect.top < 0:
            world.delete_entity(bullet_entity)
            player_tag.bullets += 1
