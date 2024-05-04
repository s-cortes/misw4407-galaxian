from pygame import display


from .prefab_base import create_sprite, get_color


def set_screen(window: dict):
    return display.set_mode((window["size"]["w"], window["size"]["h"]), 0)


def set_caption(window: dict):
    return display.set_caption(window["title"])


def get_screen_color(window: dict):
    return get_color(window, "bg_color")
