from pygame import K_LEFT, K_RIGHT, K_SPACE, K_p, K_z

from esper import World
from src.ecs.components.base import CInput, InputName


def create_intro_inputs(world: World):
    world.add_component(world.create_entity(), CInput(InputName.PLAYER_LEFT, K_LEFT))
    world.add_component(world.create_entity(), CInput(InputName.PLAYER_RIGHT, K_RIGHT))
    world.add_component(world.create_entity(), CInput(InputName.PLAYER_SPACE, K_SPACE))
    world.add_component(world.create_entity(), CInput(InputName.PLAYER_P, K_p))
    world.add_component(world.create_entity(), CInput(InputName.PLAYER_Z, K_z))
