from pygame import Color, Surface, Vector2, Rect


class CSurface:
    def __init__(self, size: Vector2, color: Color) -> None:
        self.surf: Surface = Surface(size)
        self.surf.fill(color)
        self.area: Rect = self.surf.get_rect()

    @classmethod
    def from_surface(cls, surface: Surface):
        c_surf = cls(Vector2(0, 0), Color(0, 0, 0))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf

    @staticmethod
    def get_relative_area(area: Rect, topleft: Vector2) -> Rect:
        new_rect = area.copy()
        new_rect.topleft = topleft.copy()
        return new_rect
