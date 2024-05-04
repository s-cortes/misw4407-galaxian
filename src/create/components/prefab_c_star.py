from random import choice, randint
from pygame import Color, Vector2

from esper import World
from src.create.prefab_base import create_square
from src.create.prefab_interface import get_screen_color
from src.ecs.components.tags import CTagStar
from src.ecs.components.states import CStarState


def create_star(world: World, config: dict, window: dict, index: int):
    distance = window["size"]["w"] // (config["number_of_stars"] + 2)
    pos = Vector2(distance * (index + 1), randint(0, window["size"]["h"]))
    size = Vector2(1, 1)

    show_color = Color(*choice(config["star_colors"]))
    hide_color = Color(*get_screen_color(window))
    state = CStarState(show_color, hide_color)

    vel = Vector2(0, choice(config["vertical_speed"]))
    blink_rate = choice(config["blink_rate"])

    entity = create_square(world, pos, size, vel, show_color)
    world.add_component(entity, CTagStar(blink_rate))
    world.add_component(entity, state)
    return entity
