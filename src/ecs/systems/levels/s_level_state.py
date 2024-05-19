import asyncio
from esper import World
from src.create.components.prefab_image import create_intro_image
from src.create.components.prefab_invader import (
    create_invaders_bullet_spawner,
    create_invaders_spawner,
    create_set_invaders,
)
from src.create.components.prefab_lives_indicator import create_life_indicator
from src.create.components.prefab_player import create_c_player
from src.create.components.prefab_text import (
    create_board_text,
    create_info_text,
    create_intro_text,
)
from src.ecs.components.base import CLevel
from src.ecs.components.base.c_surface import CSurface
from src.ecs.components.invaders import CInvaderBulletSpawner, CInvaderSpawner
from src.ecs.components.states import CLevelState, LevelState
from src.ecs.components.tags import (
    CTagBoard,
    CTagInvader,
    CTagInfo,
    CTagIntro,
    CTagPlayer,
)
from src.engine.services.service_locator import ServiceLocator


def system_level_state(
    world: World,
    levels_cfg: list[dict],
    player_cfg: dict,
    enemies_cfg: dict,
    intro_cfg: dict,
    board_cfg: dict,
    game_end_cfg: dict,
    lives_cfg: dict,
):
    components = world.get_components(CLevelState, CLevel)

    c_state: CLevelState
    c_level: CLevel
    for entity, (c_state, c_level) in components:
        if c_state.state == LevelState.GAME_INTRO:
            _do_game_intro(world, c_state, c_level, intro_cfg, board_cfg)
        elif c_state.state == LevelState.GAME_STARTED:
            _do_game_started_state(world, c_state, c_level, levels_cfg, player_cfg, lives_cfg)
        elif c_state.state == LevelState.LEVEL_STARTED:
            _do_level_started_state(world, c_state, c_level, levels_cfg, enemies_cfg)
        elif c_state.state == LevelState.LEVEL_WON:
            _do_level_won_state(world, c_state, c_level, levels_cfg, game_end_cfg)
        elif c_state.state == LevelState.LEVEL_LOST:
            _do_level_lost_state(world, c_state, c_level, game_end_cfg, entity)
        elif c_state.state == LevelState.GAME_LOST:
            _do_game_lost_state(world, entity, c_state, c_level)
        elif c_state.state == LevelState.GAME_WON:
            _do_game_won_state(world, entity, c_state, c_level)


def _do_game_intro(
    world: World, state: CLevelState, level: CLevel, intro_cfg: dict, board_cfg: bool
):
    if not world.get_component(CTagIntro):
        print("game intro")
        for text in intro_cfg["texts"]:
            create_intro_text(world, text)
        for img in intro_cfg["images"]:
            create_intro_image(world, img)
    if not world.get_component(CTagBoard):
        for text in board_cfg["texts"]:
            create_board_text(world, text)

    if not level.intro_active:
        state.state = LevelState.GAME_STARTED


def _do_game_started_state(
    world: World,
    state: CLevelState,
    level: CLevel,
    levels_cfg: list[dict],
    player_cfg: dict,
    lives_cfg: dict,
):
    print("game started")
    level.next_level = False
    if not level.intro_active:
        state.state = LevelState.LEVEL_STARTED
        level.current += 1
        level.next_level = True
        level.completed = False
        level.player = create_c_player(world, player_cfg, levels_cfg[level.current])
        create_life_indicator(world, lives_cfg, level.player)


def _do_level_started_state(
    world: World,
    state: CLevelState,
    level: CLevel,
    levels_cfg: list[dict],
    enemies_cfg: dict,
):
    if level.next_level:
        _set_invaders(world, level, levels_cfg, enemies_cfg)
        level.next_level = False

    if not world.get_component(CTagInvader):
        state.state = LevelState.LEVEL_WON

    player_tag: CTagPlayer = world.component_for_entity(level.player, CTagPlayer)
    if player_tag.lives <= 0:
        state.state = LevelState.LEVEL_LOST


def _do_level_won_state(
    world: World,
    state: CLevelState,
    level: CLevel,
    levels_cfg: list[dict],
    game_end_cfg: dict,
):
    level.current = level.current + 1
    _clear_invader_spawners(world)

    if level.current >= len(levels_cfg):
        state.state = LevelState.GAME_WON
        level.completed = True
        level.next_level = False

        world.delete_entity(level.player)
        level.player = None

        create_info_text(world, game_end_cfg["GAME_WON"]["text"])
    else:
        state.state = LevelState.LEVEL_STARTED
        level.next_level = True
    level.current = min(level.current, len(levels_cfg) - 1)


def _do_level_lost_state(
    world: World, state: CLevelState, level: CLevel, game_end_cfg: dict, entity: int
):
    state.state = LevelState.GAME_LOST
    level.completed = True
    level.next_level = False

    _clear_invader_spawners(world)
    create_info_text(world, game_end_cfg["GAME_OVER"]["text"])
    ServiceLocator.sounds_service.play(game_end_cfg["GAME_OVER"]["sound"])
    asyncio.ensure_future(_play_again(world, entity, state))
    _reset_score(world)


def _do_game_lost_state(world: World, entity: int, state: CLevelState, level: CLevel):
    if level.restart:
        state.state = LevelState.GAME_INTRO
        _restart_levels(world, entity)


def _do_game_won_state(world: World, entity: int, state: CLevelState, level: CLevel):
    if level.restart:
        state.state = LevelState.GAME_INTRO
        _restart_levels(world, entity)
        _reset_score(world)


def _set_invaders(
    world: World, level: CLevel, levels_cfg: list[dict], enemies_cfg: dict
):
    create_set_invaders(world, enemies_cfg, levels_cfg[level.current])
    create_invaders_spawner(world, levels_cfg[level.current])
    create_invaders_bullet_spawner(world, levels_cfg[level.current])
    level.invaders_rage = levels_cfg[level.current]["invaders_range"]


def _clear_invader_spawners(world: World):
    for entity, (_) in world.get_component(CInvaderSpawner):
        world.delete_entity(entity)
    for entity, (_) in world.get_component(CInvaderBulletSpawner):
        world.delete_entity(entity)


def _restart_levels(world: World, level_entity: int):
    for entity, (_) in world.get_component(CTagInfo):
        world.delete_entity(entity)
    world.remove_component(level_entity, CLevel)
    world.add_component(level_entity, CLevel())

async def _play_again(world: World, level_entity: int, state: CLevelState):
    await asyncio.sleep(2)
    state.state = LevelState.GAME_INTRO
    for entity, (_) in world.get_component(CTagInfo):
        world.delete_entity(entity)
    for entity, (_) in world.get_component(CTagInvader):
        world.delete_entity(entity)
    ent = world.get_component(CTagPlayer)[0][0]
    world.remove_component(ent, CTagPlayer)
    world.remove_component(ent, CSurface)
    world.remove_component(level_entity, CLevel)
    world.add_component(level_entity, CLevel())

def _reset_score(world: World):
    for entity, obj in world.get_component(CTagBoard):
        if obj.label == 'score_indicator':
            score_comp = obj
            score_entity = entity
            break
    font = ServiceLocator.fonts_service.get(score_comp.font, score_comp.size)
    score_comp.text = '0000'
    color_tuple = tuple(score_comp.color_data.values())
    surface = font.render(score_comp.text, True, color_tuple)
    surface_comp = world.component_for_entity(score_entity, CSurface)
    surface_comp.surf = surface