from pygame import Vector2

from esper import World
from src.create.prefab_base import create_sprite
from src.ecs.components.base import CSurface
from src.ecs.components.states import CIntroState
from src.ecs.components.tags import CTagIntro
from src.engine.services.service_locator import ServiceLocator


def _create_image(world: World, img: dict):
    surface = ServiceLocator.images_service.get(img["image"])
    size = surface.get_rect().size

    pos_ini = img["pos_ini"]
    pos_ini = Vector2(pos_ini[0] - (size[0] / 2), pos_ini[1] - (size[1] / 2))
    vel = Vector2(*img["velocity"])

    return create_sprite(world, pos_ini, surface, vel)


def create_intro_image(world: World, img: dict):
    entity = _create_image(world, img)

    surface = world.component_for_entity(entity, CSurface)
    size = surface.surf.get_rect().size

    pos_fin = img["pos_fin"]
    pos_fin = Vector2(pos_fin[0] - (size[0] / 2), pos_fin[1] - (size[1] / 2))
    world.add_component(entity, CTagIntro(pos_fin))
    world.add_component(entity, CIntroState())
    return entity
