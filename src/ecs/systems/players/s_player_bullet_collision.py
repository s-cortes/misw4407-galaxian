import esper
import asyncio
import pygame
from src.create.components.prefab_explosion import create_explosion
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.invaders.c_player_intangible import CIntangible
from src.ecs.components.tags.c_tag_invader_bullet import CTagInvaderBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_bullet_collision(ecs_world: esper.World, player_entity_int: int, config: tuple, death_config: dict):
    if player_entity_int is not None:
        bullet_components = ecs_world.get_components(CSurface, CTransform, CTagInvaderBullet)
        player_components = ecs_world.get_components(CSurface, CTransform, CTagPlayer)
        player_transform = ecs_world.component_for_entity(player_entity_int, CTransform)
        player_intangible = ecs_world.try_component(player_entity_int, CIntangible)
        if player_intangible:
            return
        for bullet_entity, (bullet_c_s, bullet_c_t, bullet_c_t_e) in bullet_components:
            bullet_rect = bullet_c_s.area.copy()
            bullet_rect.topleft = bullet_c_t.pos

            for player_entity, (player_c_s, player_c_t, player_c_t_e) in player_components:
                player_rect = player_c_s.area.copy()
                player_rect.topleft = player_c_t.pos

                if bullet_rect.colliderect(player_rect):
                    ecs_world.delete_entity(bullet_entity, True)
                    player_c_t_e.lives -= 1
                    original_surface = player_c_s.surf
                    player_c_s.surf = pygame.Surface((0, 0))
                    ecs_world.add_component(player_entity_int, CIntangible())
                    create_explosion(ecs_world, player_transform.pos, death_config['player'])
                    asyncio.ensure_future(restore_player_surface_after_explosion(ecs_world, player_entity, original_surface))
                    player_transform.pos.x = config[0]
                    player_transform.pos.y = config[1]


    else:
        return

async def restore_player_surface_after_explosion(ecs_world: esper.World, player_entity: int, original_surface: pygame.Surface) -> None:
    try:
        await asyncio.sleep(3)
        ecs_world.component_for_entity(player_entity, CSurface).surf = original_surface
        ecs_world.remove_component(player_entity, CIntangible)
    except:
        return