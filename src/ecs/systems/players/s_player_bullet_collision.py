import esper
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.tags.c_tag_invader_bullet import CTagInvaderBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_bullet_colision(ecs_world: esper.World):
    bullet_components = ecs_world.get_components(CSurface, CTransform, CTagInvaderBullet)
    player_components = ecs_world.get_components(CSurface, CTransform, CTagPlayer)
    #player_transform = ecs_world.component_for_entity(player_entity_int, CTransform)
    for bullet_entity, (bullet_c_s, bullet_c_t, bullet_c_t_e) in bullet_components:
        bullet_rect = bullet_c_s.area.copy()
        bullet_rect.topleft = bullet_c_t.pos

        for player_entity, (player_c_s, player_c_t, player_c_t_e) in player_components:
            player_rect = player_c_s.area.copy()
            player_rect.topleft = player_c_t.pos

            if bullet_rect.colliderect(player_rect):
                ecs_world.delete_entity(player_entity)
                ecs_world.delete_entity(bullet_entity, True)