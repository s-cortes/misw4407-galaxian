from esper import World
from src.create.components.prefab_level_assets import create_level_text, get_text_surface, create_level_image
from src.ecs.components.base import CSurface, CLevel
from src.ecs.components.states import CLevelState, LevelState
from src.ecs.components.tags.c_tag_level_assets import CTagLevelText, CTagLevelImage


def system_level_assets(world: World, level_assets: dict):
    system_level_text(world, level_assets['level_text'])
    system_level_image(world, level_assets['image'])


def system_level_text(world: World, level_text: dict):
    level_components = world.get_components(CLevel, CLevelState)
    c_level: CLevel
    c_level_state: CLevelState
    for _, (c_level, c_level_state) in level_components:
        level_texts_c = world.get_components(CSurface, CTagLevelText)
        if c_level_state.state == LevelState.GAME_INTRO:
            level_text['text'] = '01'
            for entity, (c_surface, c_level_text) in level_texts_c:
                world.delete_entity(entity, True)
        else:
            if len(level_texts_c) == 0:
                create_level_text(world, level_text)
                break
            for _, (c_surface, c_level_text) in level_texts_c:
                if c_level_text.level != c_level.current:
                    level_text['text'] = f'0{c_level.current + 1}'
                    c_surface.surf = get_text_surface(level_text)
                    c_level_text.level = c_level.current
                    break


def system_level_image(world: World, level_image: dict):
    level_components = world.get_component(CLevelState)
    c_level_state: CLevelState
    for _, (c_level_state) in level_components:
        level_images_c = world.get_component(CTagLevelImage)
        if c_level_state.state == LevelState.GAME_INTRO:
            for entity, (c_level_image) in level_images_c:
                world.delete_entity(entity, True)
        else:
            if len(level_images_c) == 0:
                create_level_image(world, level_image)
