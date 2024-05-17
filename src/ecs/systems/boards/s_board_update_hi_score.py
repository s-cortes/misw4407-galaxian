from esper import World
from src.ecs.components.base.c_surface import CSurface
from src.ecs.components.tags.c_tag_board import CTagBoard
from src.engine.services.service_locator import ServiceLocator

def system_board_update_hi_score(ecs_world: World):
    board_comps = ecs_world.get_component(CTagBoard)
    for ent, obj in board_comps:
        if obj.label == 'score_indicator':
            score_comp = ecs_world.component_for_entity(ent, CTagBoard)
            score_ent = ent

        elif obj.label == 'hi_score_indicator':
            hi_score_comp = ecs_world.component_for_entity(ent, CTagBoard)
            hi_score_ent = ent
    
    hi_score_to_int = int(hi_score_comp.text)
    score_to_int = int(score_comp.text)

    if score_to_int > hi_score_to_int:
        font = ServiceLocator.fonts_service.get(hi_score_comp.font, hi_score_comp.size)
        hi_score_comp.text = score_comp.text
        color_tuple = tuple(hi_score_comp.color_data.values())
        surface = font.render(hi_score_comp.text, True, color_tuple)
        surface_comp = ecs_world.component_for_entity(hi_score_ent, CSurface)
        surface_comp.surf = surface