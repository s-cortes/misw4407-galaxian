from esper import World
from src.create.components.prefab_invader import (
    create_invaders_bullet_spawner,
    create_invaders_spawner,
    create_set_invaders,
)
from src.create.components.prefab_player import create_c_player
from src.ecs.components.base import CLevel


def system_level_spawner(
    world: World,
    level: CLevel,
    levels_cfg: dict,
    player: dict,
    enemies_cfg: dict,
):
    if level.intro_active or not level.next_level:
        return

    level.current = level.current + 1
    level.next_level = False

    if level.current >= len(levels_cfg):
        return

    if level.player is None:
        level.player = create_c_player(world, player, levels_cfg[level.current])

    create_set_invaders(world, enemies_cfg, levels_cfg[level.current])
    create_invaders_spawner(world, levels_cfg[level.current])
    create_invaders_bullet_spawner(world, levels_cfg[level.current])
    level.invaders_rage = levels_cfg[level.current]["invaders_range"]
