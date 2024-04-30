import pygame
import esper

from src.create.prefab_creator import crear_sprite
from src.ecs.components.c_interface_state import CInterfaceState
from src.engine.service_locator import ServiceLocator


def system_interface(world:esper.World,interface_cfg:dict, text_cfg:dict ):
    for element in text_cfg.get("elementos"):
        if(element.get("value") != None):
            color_key = element["color"]
            color = pygame.Color(interface_cfg[color_key]["r"],interface_cfg[color_key]["g"],interface_cfg[color_key]["b"])
            texto_sprite = ServiceLocator.texts_service.get_sprite(
                    text_cfg["font"],
                    str(interface_cfg[element["value"]]),
                    color,
                    text_cfg["size"]
                    )
            entidad = crear_sprite(world,
                pygame.Vector2(element["pos_ini"]["x"], element["pos_ini"]["y"]),
                pygame.Vector2(text_cfg["vel"]["x"],text_cfg["vel"]["y"]),
                texto_sprite)
        else:
            color_key = element["color"]
            color = pygame.Color(interface_cfg[color_key]["r"],interface_cfg[color_key]["g"],interface_cfg[color_key]["b"])
            texto_sprite = ServiceLocator.texts_service.get_sprite(
                    text_cfg["font"],
                    element["text"],
                    color,
                    text_cfg["size"]
                    )
            entidad = crear_sprite(world,
                pygame.Vector2(element["pos_ini"]["x"], element["pos_ini"]["y"]),
                pygame.Vector2(text_cfg["vel"]["x"],text_cfg["vel"]["y"]),
                texto_sprite)
        world.add_component(entidad,CInterfaceState(pygame.Vector2(element["pos_fin"]["x"], element["pos_fin"]["y"])))
    
    letrero_surface = ServiceLocator.images_service.get("assets/img/invaders_logo_title.png")
    entidad_letrero = crear_sprite(world,
                pygame.Vector2(52, 320),
                pygame.Vector2(0, -50),
                letrero_surface)
    world.add_component(entidad_letrero,CInterfaceState(pygame.Vector2(52, 64)))
