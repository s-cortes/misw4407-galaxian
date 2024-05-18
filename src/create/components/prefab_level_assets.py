from pygame import Vector2
from pygame import Color
from esper import World
from src.create.prefab_base import create_sprite
from src.ecs.components.tags.c_tag_level_assets import CTagLevelImage, CTagLevelText
from src.engine.services import ServiceLocator


def create_level_image(world: World, level_image_cfg: dict):

    surface = ServiceLocator.images_service.get(level_image_cfg["image"])
    pos = Vector2(level_image_cfg["position"]["x"], level_image_cfg["position"]["y"])
    vel = Vector2(0, 0)
    entity = create_sprite(world, pos, surface, vel)

    world.add_component(entity, CTagLevelImage())


def create_level_text(world: World, level_text_cfg: dict):
    surface = get_text_surface(level_text_cfg)
    pos = Vector2(level_text_cfg['position']['x'], level_text_cfg['position']['y'])
    vel = Vector2(0, 0)

    entity = create_sprite(world, pos, surface, vel)
    world.add_component(entity, CTagLevelText())


def get_text_surface(level_text_cfg: dict):
    font = ServiceLocator.fonts_service.get(level_text_cfg["font"], level_text_cfg["size"])
    return font.render(
        level_text_cfg["text"],
        True,
        Color(level_text_cfg['color']['r'], level_text_cfg['color']['g'], level_text_cfg['color']['b']))