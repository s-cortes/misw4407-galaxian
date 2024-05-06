from pygame.font import Font


class FontsService:
    def __init__(self) -> None:
        self._fonts: dict[str, dict[int, Font]] = dict()

    def get(self, path: str, size: int) -> Font:
        if path not in self._fonts:
            self._fonts[path] = dict()
        if size not in self._fonts[path]:
            self._fonts[path][size] = Font(path, size)
        return self._fonts[path][size]
