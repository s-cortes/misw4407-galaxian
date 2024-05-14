import esper
import random
from src.ecs.components.invaders.c_invader_spawner import CInvaderSpawner
from src.ecs.components.tags.c_tag_invader import CTagInvader
from src.engine.services import ServiceLocator


def system_invader_spawner(ecs_world: esper.World):
    components = ecs_world.get_component(CInvaderSpawner)
    c_spawner: CInvaderSpawner
    for _, (c_spawner) in components:
        if c_spawner.time >= c_spawner.spawn_time and c_spawner.spawn_is_on is False:
            invaders_components = ecs_world.get_component(CTagInvader)
            spawner_size = min(c_spawner.spawner_size, len(invaders_components))
            selected_invaders = random.sample(range(0, len(invaders_components)), spawner_size)
            c_invader: CTagInvader
            for index in selected_invaders:
                invaders_components[index][1].selected = True
                ServiceLocator.sounds_service.play(invaders_components[index][1].launch_sound)
            c_spawner.spawn_is_on = True


def system_update_invaders_spawner_time(ecs_world: esper.World, delta_time: float):
    components = ecs_world.get_component(CInvaderSpawner)
    c_spawner: CInvaderSpawner
    for _, (c_spawner) in components:
        if c_spawner.spawn_is_on is False:
            c_spawner.time += delta_time
