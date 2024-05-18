import esper
import random

from src.create.components.prefab_invader import create_invader_bullet
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.invaders.c_invader_bullet_spawner import CInvaderBulletSpawner
from src.ecs.components.states.c_invader_state import CInvaderState, InvaderState
from src.ecs.components.tags.c_tag_invader import CTagInvader


def system_invader_bullet_spawner(ecs_world: esper.World, level_cfg: dict):

    components = ecs_world.get_component(CInvaderBulletSpawner)
    c_bullet_spawner: CInvaderBulletSpawner
    for _, (c_bullet_spawner) in components:
        if c_bullet_spawner.time >= c_bullet_spawner.spawn_time:
            invaders_components = ecs_world.get_components(CSurface, CTransform, CTagInvader, CInvaderState)
            max_shots = min(c_bullet_spawner.shooters, len(invaders_components))
            selected_invaders = random.sample(range(0, len(invaders_components)), max_shots)

            for index in selected_invaders:
                create_invader_bullet(ecs_world, level_cfg['invader_bullet'], invaders_components[index][1][1])

            c_invader_state: CInvaderState
            for _, (c_surface, c_transform, c_tag_invader, c_invader_state) in invaders_components:
                if c_invader_state.state == InvaderState.ATTACK:
                    create_invader_bullet(ecs_world, level_cfg['invader_bullet'], c_transform)

            c_bullet_spawner.time = 0.0


def system_update_invaders_bullet_spawner_time(ecs_world: esper.World, delta_time: float):
    components = ecs_world.get_component(CInvaderBulletSpawner)
    c_spawner: CInvaderBulletSpawner
    for _, (c_spawner) in components:
        c_spawner.time += delta_time

