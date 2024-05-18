import esper
from src.create.components.prefab_explosion import create_explosion
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.states.c_score_state import CScoreState, ScoreState
from src.ecs.components.tags.c_tag_board import CTagBoard
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_invader import CTagInvader
from src.engine.services.service_locator import ServiceLocator

def system_invader_bullet_collision(ecs_world: esper.World, death_config: dict):
    bullet_components = ecs_world.get_components(CSurface, CTransform, CTagPlayerBullet)
    invader_components = ecs_world.get_components(CSurface, CTransform, CTagInvader)
    for bullet_entity, (bullet_c_s, bullet_c_t, bullet_c_t_e) in bullet_components:
        bullet_rect = bullet_c_s.area.copy()
        bullet_rect.topleft = bullet_c_t.pos

        for enemy_entity, (enemy_c_s, enemy_c_t, enemy_c_t_e) in invader_components:
            enemy_rect = enemy_c_s.area.copy()
            enemy_rect.topleft = enemy_c_t.pos

            if bullet_rect.colliderect(enemy_rect):
                create_explosion(ecs_world, enemy_c_t.pos, death_config['enemy'])
                ecs_world.delete_entity(bullet_entity)
                _update_score(ecs_world, enemy_entity)
                ecs_world.delete_entity(enemy_entity)

def _update_score(ecs_world: esper.World, enemy_ent: int):
    c_score = ecs_world.get_component(CScoreState)
    if c_score[0][1].state == ScoreState.ON:
        enemy_comp = ecs_world.component_for_entity(enemy_ent, CTagInvader)
        board_comps = ecs_world.get_component(CTagBoard)
        
        for ent, obj in board_comps:
            if obj.label == 'score_indicator':
                score_comp = ecs_world.component_for_entity(ent, CTagBoard)
                score_ent = ent
                break

        font = ServiceLocator.fonts_service.get(score_comp.font, score_comp.size)
        score_to_int = int(score_comp.text)
        new_score = score_to_int + enemy_comp.invader_points
        score_comp.text = str(new_score)
        color_tuple = tuple(score_comp.color_data.values())
        surface = font.render(score_comp.text, True, color_tuple)
        surface_comp = ecs_world.component_for_entity(score_ent, CSurface)
        surface_comp.surf = surface
    else:
        return