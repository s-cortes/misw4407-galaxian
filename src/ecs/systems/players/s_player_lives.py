import pygame
import esper
from src.ecs.components.tags.c_tag_lives import CTagLives
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_lives(ecs_world: esper.World, player_entity: int):
    try:
        l_comp = ecs_world.component_for_entity(player_entity, CTagLives)
        p_comp = ecs_world.component_for_entity(player_entity, CTagPlayer)
        if p_comp.lives < len(l_comp.ents):
            ent = min(l_comp.ents)
            print('perdi una vida')
            ecs_world.delete_entity(ent, True)
            l_comp.ents.remove(min(l_comp.ents))
    except:
        return
