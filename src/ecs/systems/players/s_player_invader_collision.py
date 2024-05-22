import esper
import asyncio
import pygame
from src.create.components.prefab_explosion import create_explosion
from src.ecs.components.base import CSurface, CTransform
from src.ecs.components.invaders.c_player_intangible import CIntangible
from src.ecs.components.tags import CTagInvader
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_player_invader_collision(ecs_world: esper.World, player_entity_int: int, config: tuple, death_config: dict):
    if player_entity_int is not None:
        invaders_components = ecs_world.get_components(CSurface, CTransform, CTagInvader)
        player_components = ecs_world.get_components(CSurface, CTransform, CTagPlayer)
        player_transform = ecs_world.component_for_entity(player_entity_int, CTransform)
        player_intangible = ecs_world.try_component(player_entity_int, CIntangible)
        if player_intangible:
            return
        for invader_entity, (invader_c_s, invader_c_t, invader_c) in invaders_components:
            invader_rect = invader_c_s.area.copy()
            invader_rect.topleft = invader_c_t.pos

            for player_entity, (player_c_s, player_c_t, player_c_t_e) in player_components:
                player_rect = player_c_s.area.copy()
                player_rect.topleft = player_c_t.pos

                if invader_rect.colliderect(player_rect):
                    ecs_world.delete_entity(invader_entity, True)
                    player_c_t_e.lives -= 1
                    original_surface = player_c_s.surf
                    player_c_s.surf = pygame.Surface((0, 0))
                    ecs_world.add_component(player_entity_int, CIntangible())
                    create_explosion(ecs_world, player_transform.pos, death_config['player'])
                    asyncio.ensure_future(restore_player_surface_after_explosion(ecs_world, player_entity, original_surface, config))
                    player_transform.pos.x = config['player']['position'][0]
                    player_transform.pos.y = config['player']['position'][1]
    else:
        return

async def restore_player_surface_after_explosion(ecs_world: esper.World, player_entity: int, original_surface: pygame.Surface, config: dict) -> None:
    try:
        await asyncio.sleep(3)
        ecs_world.component_for_entity(player_entity, CSurface).surf = original_surface
        await asyncio.sleep(0.3)
        try:
            ecs_world.remove_component(player_entity, CIntangible)
        except:
            pass
        ecs_world.component_for_entity(player_entity, CTagPlayer).bullets = config['player']['max_bullets']
    except:
        return