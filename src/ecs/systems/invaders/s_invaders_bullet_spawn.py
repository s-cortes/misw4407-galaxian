import esper
import random

from src.create.components.prefab_invader import create_invader_bullet
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.invaders.c_invader_bullet_spawner import CInvaderBulletSpawner
from src.ecs.components.tags.c_tag_invader import CTagInvader


def system_invader_bullet_spawner(ecs_world: esper.World, level_cfg: dict, player_entity: int):

    components = ecs_world.get_component(CInvaderBulletSpawner)
    c_bullet_spawner: CInvaderBulletSpawner
    for _, (c_bullet_spawner) in components:
        if c_bullet_spawner.time >= c_bullet_spawner.spawn_time:
            invaders_components = ecs_world.get_components(CSurface, CTransform, CTagInvader)
            bullet_spawner = min(c_bullet_spawner.shooters, len(invaders_components))
            selected_invaders = random.sample(range(0, len(invaders_components)), c_bullet_spawner.shooters)

            for index in selected_invaders:
                create_invader_bullet(ecs_world, level_cfg['invader_bullet'], player_entity,
                                      invaders_components[index][1][0], invaders_components[index][1][1])

            c_bullet_spawner.time = 0.0


def system_update_invaders_bullet_spawner_time(ecs_world: esper.World, delta_time: float):
    components = ecs_world.get_component(CInvaderBulletSpawner)
    c_spawner: CInvaderBulletSpawner
    for _, (c_spawner) in components:
        c_spawner.time += delta_time

