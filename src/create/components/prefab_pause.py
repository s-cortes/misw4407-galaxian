from esper import World
from src.create.components.prefab_text import _create_text
from src.engine.services.service_locator import ServiceLocator


def create_pause(world: World, config: dict):
    ServiceLocator.sounds_service.play(config["sound"])
    return _create_text(world, config["text"])
