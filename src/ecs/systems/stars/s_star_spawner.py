from esper import World
from src.create.components.prefab_c_star import create_star


def sytem_star_spawner(world: World, config: dict, window: dict):
    if config["count"] < config["number_of_stars"]:
        create_star(world, config, window, config["count"])
        config["count"] = config["count"] + 1
