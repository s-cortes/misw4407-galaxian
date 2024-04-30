import pygame
import esper
from src.ecs.components.c_interface_state import CInterfaceState, InterfaceState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_interface_state(world:esper.World):
    components = world.get_components(CTransform, CInterfaceState, CVelocity)
    for _, (c_t, c_pst, c_v) in components:
        if c_pst.state == InterfaceState.LOADING:
            _do_loading_state(c_t, c_pst, c_v)
        elif c_pst.state == InterfaceState.LOADED:
            _do_loaded_state(c_t,c_pst, c_v)
        elif c_pst.state == InterfaceState.GAMING:
            _do_gaming_state(c_t, c_pst,c_v)

def _do_loading_state(c_t: CTransform, c_pst: CInterfaceState, c_v: CVelocity):
    distancia_restante = c_pst.fin.distance_to(c_t.pos)
    if(distancia_restante <= 2):
        c_t.pos.xy = c_pst.fin.xy
        c_v.vel = pygame.Vector2(0,0)
        c_pst.state = InterfaceState.LOADED
        

def _do_loaded_state(c_t: CTransform, c_pst: CInterfaceState, c_v: CVelocity):
    pass

def _do_gaming_state(c_t: CTransform,c_pst: CInterfaceState, c_v: CVelocity):
    pass