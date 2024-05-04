from pygame import K_z

from esper import World
from src.ecs.components.base import CInput


def create_intro_inputs(world: World):
    down = world.create_entity()
    world.add_component(down, CInput("PLAYER_Z", K_z))
