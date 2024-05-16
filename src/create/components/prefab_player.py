from pygame import Color, Vector2
from esper import World
from src.create.prefab_base import create_sprite, create_square
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.states import CPlayerState
from src.ecs.components.tags import CTagPlayer, CTagPlayerBullet
from src.engine.services import ServiceLocator
from src.ecs.components.base import CLives
from src.ecs.components.base import CLivesIndicator


def create_c_player(world: World, config: dict, level_cfg: dict) -> int:
    spawn = level_cfg["player"]

    surface = ServiceLocator.images_service.get(config["image"])
    size = surface.get_rect().size

    pos = spawn["position"]
    pos = Vector2(pos[0] - (size[0] / 2), pos[1] - (size[1] / 2))

    velocity = config["input_velocity"]
    vel = Vector2(velocity, velocity)

    entity = create_sprite(world, pos, surface, vel)
    world.add_component(entity, CTagPlayer(spawn["max_bullets"]))
    world.add_component(entity, CPlayerState())
    world.add_component(entity, CLives(spawn["lives"]["max_lives"]))
    create_life_indicators(world, spawn["lives"])
    return entity


def create_c_player_bullet(world: World, entity_p: int, player_cfg: dict):
    config = player_cfg["bullet"]
    ctp = world.component_for_entity(entity_p, CTransform)
    stp = world.component_for_entity(entity_p, CSurface)

    size = Vector2(2, 5)
    pos = Vector2(
        ctp.pos.x + (stp.area.w / 2) - (size.x / 2),
        ctp.pos.y + (stp.area.h / 2) - (size.y / 2),
    )
    vel = Vector2(0, -config["velocity"])
    color = Color(*config["color"])

    entity = create_square(world, pos, size, vel, color)
    world.add_component(entity, CTagPlayerBullet())

    ServiceLocator.sounds_service.play(config["sound"])
    return entity

def create_life_indicators(world: World, lives_cfg: dict):
    surface = ServiceLocator.images_service.get(lives_cfg["img"])
    size = surface.get_rect().size
    pos = Vector2(lives_cfg["position"]["x"], lives_cfg["position"]["y"])
    for i in range(lives_cfg["max_lives"]):
        life_pos = pos + Vector2(i * (size[0] + 5), 0)
        life_entity = create_sprite(world, life_pos, surface, Vector2(0, 0))
        world.add_component(life_entity, CLivesIndicator())