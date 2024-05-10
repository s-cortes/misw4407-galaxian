from esper import World
from src.create.components.prefab_invader import create_set_invaders, create_invaders_spawner, \
    create_invaders_bullet_spawner
from src.create.components.prefab_player import create_c_player
from src.ecs.components.tags import CTagPlayer


def system_level_spawner(
    world: World, intro: bool, level: dict, levels_cfg: dict, player: dict,
    enemies_cfg: dict
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

    create_set_invaders(world, enemies_cfg, levels_cfg[level["current"]])
    create_invaders_spawner(world, levels_cfg[level["current"]])
    create_invaders_bullet_spawner(world, levels_cfg[level["current"]])
    level['invaders_range'] = levels_cfg[level["current"]]['invaders_range']
    level['invaders_velocity'] = levels_cfg[level["current"]]['invaders_velocity']