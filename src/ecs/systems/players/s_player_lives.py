import pygame
import esper
from src.ecs.components.base.c_lives import CLives

def system_handle_lives(ecs_world: esper.World, player_entity: int):
    if player_entity is not None:
        player_lives = ecs_world.component_for_entity(player_entity, CLives)
        if player_lives.lives <= 0:
            print("Game Over")
            pygame.quit()
            exit()
    else:
        return
