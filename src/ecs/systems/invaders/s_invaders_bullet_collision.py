import esper
from src.create.components.prefab_explosion import create_explosion
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_invader import CTagInvader

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
                ecs_world.delete_entity(enemy_entity)
