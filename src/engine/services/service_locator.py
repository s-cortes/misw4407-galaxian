from .images_service import ImagesService
from .sounds_service import SoundsService
from .font_service import FontsService


class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsService()
    fonts_service = FontsService()
