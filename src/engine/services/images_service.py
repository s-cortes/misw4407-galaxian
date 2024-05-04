from pygame import Surface, image


class ImagesService:
    def __init__(self) -> None:
        self._images: dict[str, Surface] = dict()

    def get(self, path: str) -> Surface:
        if path not in self._images:
            self._images[path] = image.load(path).convert_alpha()
        return self._images[path]
