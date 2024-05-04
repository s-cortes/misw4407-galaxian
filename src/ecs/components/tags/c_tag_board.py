from enum import Enum


class TagBoardType(Enum):
    LABEL = 0
    VALUE = 1


class CTagBoard:
    def __init__(self, pos_fin: tuple, text:str, tipo: int) -> None:
        self.pos_fin = pos_fin
        self.minimum_distance = 5
        
        self.text = text
        self.tipo = TagBoardType(tipo)
