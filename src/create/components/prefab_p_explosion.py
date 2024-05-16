import pygame
import esper
from src.create.prefab_base import create_sprite
from src.ecs.components.base.c_animation import CAnimation
from src.ecs.components.tags.c_tag_player_explosion import CTagPlayerExplosion
from src.engine.services.service_locator import ServiceLocator


def create_explosion(ecs_world: esper.World, position, config: dict):
    surface = ServiceLocator.images_service.get(config["image"])
    entity = create_sprite(ecs_world, position.copy(), surface, pygame.Vector2(0, 0))
    ecs_world.add_component(entity, CTagPlayerExplosion())
    ecs_world.add_component(entity, CAnimation(config['animations']))
    ServiceLocator.sounds_service.play(config['sound'])

