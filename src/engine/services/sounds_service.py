import pygame

class SoundsService:
    def __init__(self):
        self.sounds = {}

    def play(self, path:str):
        if path not in self.sounds:
            self.sounds[path] = pygame.mixer.Sound(path)
            #self.sounds[path] = pygame.mixer_music.load()
        self.sounds[path].play()