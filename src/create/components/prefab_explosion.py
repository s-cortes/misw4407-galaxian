import asyncio
import pygame
import esper
from src.create.prefab_base import create_sprite
from src.ecs.components.base.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.engine.services.service_locator import ServiceLocator


def create_explosion(ecs_world: esper.World, position, config: dict):
    surface = ServiceLocator.images_service.get(config["image"])
    entity = create_sprite(ecs_world, position.copy(), surface, pygame.Vector2(0, 0))
    ecs_world.add_component(entity, CTagExplosion())
    ecs_world.add_component(entity, CAnimation(config['animations']))
    ServiceLocator.sounds_service.play(config['sound'])
    total_animation_time = 1
    asyncio.ensure_future(_remove_explosion_after_delay(ecs_world, entity, total_animation_time))


async def _remove_explosion_after_delay(ecs_world: esper.World, entity: int, delay: float) -> None:
    await asyncio.sleep(delay)
    ecs_world.delete_entity(entity)
