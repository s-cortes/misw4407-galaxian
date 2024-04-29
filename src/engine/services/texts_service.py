import pygame

class TextsService:
    def __init__(self):
        self.fonts = {}

    def show(self, font:str, text:str, color:pygame.Color, size:int, pantalla:pygame.Surface, pos:tuple):
        if font not in self.fonts:
            self.fonts[font] = pygame.font.Font(font, size)
        tipo_letra = self.fonts[font]
        superficie = tipo_letra.render(text,True, color)
        rectangulo = superficie.get_rect()
        rectangulo.topleft = pos
        pantalla.blit(superficie,rectangulo)

    def get_sprite(self, font:str, text:str, color:pygame.Color, size:int):
        if font not in self.fonts:
            self.fonts[font] = pygame.font.Font(font, size)
        tipo_letra = self.fonts[font]
        superficie = tipo_letra.render(text,True, color)
        return superficie