from pygame import Vector2
from esper import World
from src.create.prefab_base import create_sprite
from src.ecs.components.tags.c_tag_lives import CTagLives
from src.engine.services import ServiceLocator

def create_life_indicator(world: World, config: dict, player_ent: int):
    image: str = config['image']
    pos_x: int = config['position']['x']
    pos_y: int = config['position']['y']
    list_ents: list = []
    surface = ServiceLocator.images_service.get(image)
    size = surface.get_rect().size
    pos = Vector2(pos_x, pos_y)
    vel = Vector2(0, 0)
    for i in range(config['lives']):
        life_pos = pos + Vector2(i * (size[0] + 5), 0)
        entity = create_sprite(world, life_pos, surface, vel)
        list_ents.append(entity)
    world.add_component(player_ent, CTagLives(config['lives'], list_ents))
    return entity
