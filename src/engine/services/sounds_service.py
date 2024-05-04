from pygame.mixer import Sound


class SoundsService:
    def __init__(self) -> None:
        self._sounds: dict[str, Sound] = dict()

    def play(self, path: str) -> None:
        if path not in self._sounds:
            self._sounds[path] = Sound(path)
        self._sounds[path].play()
