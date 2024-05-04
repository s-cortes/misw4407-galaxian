from pygame import Vector2

from esper import World
from src.create.prefab_base import create_sprite, get_color
from src.ecs.components.base import CSurface
from src.ecs.components.states import CBoardState, CIntroState
from src.ecs.components.tags import CTagBoard, CTagIntro
from src.engine.services.service_locator import ServiceLocator


def _create_text(world: World, text: dict):
    font = ServiceLocator.fonts_service.get(text["font"], text["size"])
    surface = font.render(text["text"], True, get_color(text, "color"))
    size = surface.get_rect().size

    pos_ini = text["pos_ini"]
    pos_ini = Vector2(pos_ini[0] - (size[0] / 2), pos_ini[1] - (size[1] / 2))
    vel = Vector2(*text["velocity"])

    return create_sprite(world, pos_ini, surface, vel)


def create_intro_text(world: World, text: dict):
    entity = _create_text(world, text)

    surface = world.component_for_entity(entity, CSurface)
    size = surface.surf.get_rect().size

    pos_fin = text["pos_fin"]
    pos_fin = Vector2(pos_fin[0] - (size[0] / 2), pos_fin[1] - (size[1] / 2))
    world.add_component(entity, CTagIntro(pos_fin))
    world.add_component(entity, CIntroState())
    return entity


def create_board_text(world: World, text: dict):
    entity = _create_text(world, text)

    surface = world.component_for_entity(entity, CSurface)
    size = surface.surf.get_rect().size

    pos_fin = text["pos_fin"]
    pos_fin = Vector2(pos_fin[0] - (size[0] / 2), pos_fin[1] - (size[1] / 2))
    world.add_component(entity, CTagBoard(pos_fin, text["text"], text["type"]))
    world.add_component(entity, CBoardState())
    return entity
