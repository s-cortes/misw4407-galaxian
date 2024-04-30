from enum import Enum
import pygame

class CInterfaceState:
    def __init__(self, fin:pygame.Vector2):
        self.state = InterfaceState.LOADING
        self.fin = fin

class InterfaceState(Enum):
    LOADING = 0
    LOADED = 1
    GAMING = 2