import pygame
from pygame import Vector2
from esper import World
from src.create.prefab_base import create_sprite, create_square
from src.ecs.components.base import CAnimation, CSurface, CTransform, CVelocity
from src.ecs.components.invaders.c_invader_bullet_spawner import CInvaderBulletSpawner
from src.ecs.components.invaders.c_invader_spawner import CInvaderSpawner
from src.ecs.components.states.c_invader_state import CInvaderState
from src.ecs.components.tags.c_tag_invader import CTagInvader
from src.ecs.components.tags.c_tag_invader_bullet import CTagInvaderBullet
from src.engine.services import ServiceLocator
import esper


def create_set_invaders(world: World, enemies_cfg: dict, level_cfg: dict):
    for row in level_cfg['enemies']:
        position = Vector2(row['start_position']['x'],
                           row['start_position']['y'])

        for _ in range(row['amount']):
            create_c_invader(world, enemies_cfg[row['type']], row, position)
            position.x += row['gap']


def create_c_invader(world: World, invader_cfg: dict,
                     row_cfg: dict, position: pygame.Vector2):
    surface = ServiceLocator.images_service.get(invader_cfg["image"])
    single_surface = ServiceLocator.images_service.get(invader_cfg["image_single"])

    entity = create_sprite(world, position.copy(), surface, Vector2(0, 0))

    attack_velocity = Vector2(row_cfg['attack_velocity']['x'],
                              row_cfg['attack_velocity']['y'])

    move_velocity = Vector2(row_cfg['move_velocity']['x'],
                            row_cfg['move_velocity']['y'])

    return_velocity = Vector2(row_cfg['return_velocity']['x'],
                              row_cfg['return_velocity']['y'])

    c_invader = CTagInvader(position.copy(), attack_velocity, invader_cfg['angular_velocity'],
                            return_velocity, move_velocity, surface.copy(), single_surface.copy())

    world.add_component(entity, c_invader)
    world.add_component(entity, CAnimation(invader_cfg['animations']))
    world.add_component(entity, CInvaderState())


def create_invaders_spawner(world: World, level_cfg: dict):
    components = world.get_component(CInvaderSpawner)
    for entity, (c_invader_spawner) in components:
        world.delete_entity(entity, True)

    entity = world.create_entity()

    c_invader_spawner = CInvaderSpawner(level_cfg['invaders_spawner'])
    world.add_component(entity, c_invader_spawner)


def create_invaders_bullet_spawner(world: World, level_cfg: dict):
    components = world.get_component(CInvaderBulletSpawner)
    for entity, (c_invader_spawner) in components:
        world.delete_entity(entity, True)

    entity = world.create_entity()

    c_invader_bullet_spawner = CInvaderBulletSpawner(level_cfg['invaders_bullet_spawner'])
    world.add_component(entity, c_invader_bullet_spawner)


def create_invader_bullet(ecs_world: esper.World, bullet_cfg: dict, player_entity: int,
                          invader_surface: CSurface, invader_transform: CTransform):

    bullet_position = invader_transform.pos.copy()
    bullet_size = pygame.Vector2(bullet_cfg['size']['x'], bullet_cfg['size']['y'])
    bullet_color = pygame.Color(bullet_cfg['color']['r'], bullet_cfg['color']['g'], bullet_cfg['color']['b'])

    player_transform: CTransform = ecs_world.component_for_entity(player_entity, CTransform)

    b_c_transform = CTransform(bullet_position)

    target_position = player_transform.pos.copy()

    velocity_normal = pygame.Vector2(
        (target_position.x - b_c_transform.pos.x),
        (target_position.y - b_c_transform.pos.y)).normalize()
    bullet_velocity = (velocity_normal * bullet_cfg['velocity'])

    entity = create_square(ecs_world, bullet_position, bullet_size, bullet_velocity, bullet_color)

    ecs_world.add_component(entity, CTagInvaderBullet())
