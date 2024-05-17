from pygame import Color, Vector2
from esper import World
from src.create.prefab_base import create_sprite, create_square
from src.ecs.components.base import CSurface, CTransform, CLevel
from src.ecs.components.states import CLevelState, CPlayerState
from src.ecs.components.tags import CTagPlayer, CTagPlayerBullet
from src.engine.services import ServiceLocator


def create_c_level(world: World):
    entity = world.create_entity()
    world.add_component(entity, CLevel())
    world.add_component(entity, CLevelState())
    return entity


def create_c_player(world: World, config: dict, level_cfg: dict) -> int:
    spawn = level_cfg["player"]

    surface = ServiceLocator.images_service.get(config["image"])
    size = surface.get_rect().size

    pos = spawn["position"]
    pos = Vector2(pos[0] - (size[0] / 2), pos[1] - (size[1] / 2))

    velocity = config["input_velocity"]
    vel = Vector2(velocity, velocity)

    entity = create_sprite(world, pos, surface, vel)
    world.add_component(entity, CTagPlayer(spawn["max_bullets"], 3))
    world.add_component(entity, CPlayerState())
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
