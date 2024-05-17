import esper
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.tags.c_tag_board import CTagBoard
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_invader import CTagInvader
from src.create.components.prefab_i_explosion import create_explosion
from src.create.prefab_base import get_color
from src.engine.services.service_locator import ServiceLocator

def system_invader_bullet_collision(ecs_world: esper.World, enemy_config: dict, config: dict):
    bullet_components = ecs_world.get_components(CSurface, CTransform, CTagPlayerBullet)
    invader_components = ecs_world.get_components(CSurface, CTransform, CTagInvader)
    for bullet_entity, (bullet_c_s, bullet_c_t, bullet_c_t_e) in bullet_components:
        bullet_rect = bullet_c_s.area.copy()
        bullet_rect.topleft = bullet_c_t.pos

        for enemy_entity, (enemy_c_s, enemy_c_t, enemy_c_t_e) in invader_components:
            enemy_rect = enemy_c_s.area.copy()
            enemy_rect.topleft = enemy_c_t.pos

            if bullet_rect.colliderect(enemy_rect):
                ecs_world.delete_entity(bullet_entity, True)
                create_explosion(ecs_world, enemy_c_t.pos, enemy_config['death'])
                update_score(ecs_world, config, enemy_entity)
                ecs_world.delete_entity(enemy_entity)

def update_score(ecs_world: esper.World, config: dict, enemy_ent: int):
    enemy_comp = ecs_world.component_for_entity(enemy_ent, CTagInvader)
    score_ent = config['ent']
    font = ServiceLocator.fonts_service.get(config["font"], config["size"])
    score_comp = ecs_world.component_for_entity(score_ent, CTagBoard)
    score_to_int = int(score_comp.text)
    new_score = score_to_int + enemy_comp.invader_points
    score_comp.text = str(new_score)
    config['text'] = score_comp.text
    surface = font.render(config["text"], True, get_color(config, "color"))
    surface_comp = ecs_world.component_for_entity(score_ent, CSurface)
    surface_comp.surf = surface