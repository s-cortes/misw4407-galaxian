from esper import World
from src.create.components.prefab_player import create_c_player
from src.ecs.components.tags import CTagPlayer


def system_level_spawner(
    world: World, intro: bool, level: dict, levels_cfg: dict, player: dict
):
    if intro or not level["ended"]:
        return

    level["current"] = level["current"] + 1
    level["ended"] = False

    if level["current"] >= len(levels_cfg):
        return

    if level["player"] is None:
        level["player"] = create_c_player(world, player, levels_cfg[level["current"]])
        level["player_tag"] = world.component_for_entity(level["player"], CTagPlayer)
