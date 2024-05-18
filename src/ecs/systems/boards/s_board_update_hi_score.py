from esper import World
from src.ecs.components.base.c_surface import CSurface
from src.ecs.components.states.c_score_state import CScoreState, ScoreState
from src.ecs.components.tags.c_tag_board import CTagBoard
from src.engine.services.service_locator import ServiceLocator

def system_board_update_hi_score(ecs_world: World):
    try:
        board_comps = ecs_world.get_component(CTagBoard)
        c_score = ecs_world.get_component(CScoreState)
        if c_score[0][1].state == ScoreState.ON:
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
                color_tuple = tuple(hi_score_comp.color_data.values())
                if hi_score_to_int < 5000:
                    hi_score_comp.text = score_comp.text
                    surface = font.render(hi_score_comp.text, True, color_tuple)
                    surface_comp = ecs_world.component_for_entity(hi_score_ent, CSurface)
                    surface_comp.surf = surface
                else:
                    hi_score_comp.text = '5000'
                    score_comp.text = hi_score_comp.text

                    h_surface = font.render(hi_score_comp.text, True, color_tuple)
                    h_surface_comp = ecs_world.component_for_entity(hi_score_ent, CSurface)
                    h_surface_comp.surf = h_surface

                    s_surface = font.render(hi_score_comp.text, True, color_tuple)
                    s_surface_comp = ecs_world.component_for_entity(score_ent, CSurface)
                    s_surface_comp.surf = s_surface

                    c_score[0][1].state = ScoreState.OFF
        else:
            return
    except:
        return