from esper import World
from src.create.prefab_base import get_color
from src.ecs.components.base.c_surface import CSurface
from src.ecs.components.tags.c_tag_board import CTagBoard
from src.engine.services.service_locator import ServiceLocator

def system_board_update_hi_score(world: World, player_score_ent: int, hi_score_config: dict):
    hi_score_ent = hi_score_config['ent']
    hi_score_comp = world.component_for_entity(hi_score_ent, CTagBoard)
    score_comp = world.component_for_entity(player_score_ent, CTagBoard)
    hi_score_to_int = int(hi_score_comp.text)
    score_to_int = int(score_comp.text)
    if score_to_int > hi_score_to_int:
        font = ServiceLocator.fonts_service.get(hi_score_config["font"], hi_score_config["size"])
        hi_score_comp.text = score_comp.text
        hi_score_config['text'] = hi_score_comp.text
        surface = font.render(hi_score_config["text"], True, get_color(hi_score_config, "color"))
        surface_comp = world.component_for_entity(hi_score_ent, CSurface)
        surface_comp.surf = surface