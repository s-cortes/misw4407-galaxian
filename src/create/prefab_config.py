import json

from .prefab_base import get_color

WINDOW_CONFIG_PATH = "assets/cfg/window.json"
INTERFACE_CONFIG_PATH = "assets/cfg/interface.json"
INTRO_TEXT_CONFIG_PATH = "assets/cfg/intro_text.json"
BOARD_TEXT_CONFIG_PATH = "assets/cfg/board_text.json"
STARFIELD_CONFIG_PATH = "assets/cfg/starfield.json"
LEVELS_CONFIG_PATH = "assets/cfg/levels.json"
PLAYER_CONFIG_PATH = "assets/cfg/player.json"
ENEMIES_CONFIG_PATH = "assets/cfg/enemies.json"


def _get_configuration(path: str) -> dict:
    config: dict
    with open(path) as f:
        config = json.load(f)
    return config


def configure_window() -> dict:
    return _get_configuration(WINDOW_CONFIG_PATH)


def configure_interface() -> dict:
    return _get_configuration(INTERFACE_CONFIG_PATH)


def _transform_text_data(config: dict, interface: dict):
    for text in config["texts"]:
        text["text"] = str(interface.get(text["text"], text["text"]))
        text["color"] = interface[text["color"]]
        text["pos_ini"] = (text["pos_ini"]["x"], text["pos_ini"]["y"])
        text["pos_fin"] = (text["pos_fin"]["x"], text["pos_fin"]["y"])
        text["velocity"] = (text["velocity"]["x"], text["velocity"]["y"])


def _transform_image_data(config: dict):
    for img in config["images"]:
        img["pos_ini"] = (img["pos_ini"]["x"], img["pos_ini"]["y"])
        img["pos_fin"] = (img["pos_fin"]["x"], img["pos_fin"]["y"])
        img["velocity"] = (img["velocity"]["x"], img["velocity"]["y"])


def configure_intro_text(interface: dict) -> dict:
    config: dict = _get_configuration(INTRO_TEXT_CONFIG_PATH)
    _transform_text_data(config, interface)
    _transform_image_data(config)
    return config


def configure_board_text(interface: dict) -> dict:
    config: dict = _get_configuration(BOARD_TEXT_CONFIG_PATH)
    _transform_text_data(config, interface)
    return config


def configure_starfield() -> dict:
    config = _get_configuration(STARFIELD_CONFIG_PATH)
    config["star_colors"] = [get_color(c) for c in config["star_colors"]]
    config["vertical_speed"] = (
        config["vertical_speed"]["min"],
        config["vertical_speed"]["max"],
    )
    config["blink_rate"] = (
        config["blink_rate"]["min"],
        config["blink_rate"]["max"],
    )
    config["count"] = 0
    return config


def configure_levels() -> dict:
    config = _get_configuration(LEVELS_CONFIG_PATH)
    for level in config:
        level["player"]["position"] = (
            level["player"]["position"]["x"],
            level["player"]["position"]["y"],
        )
        for invader in level["invaders"]:
            invader["position"] = (
                invader["position"]["x"],
                invader["position"]["y"],
            )
    return config


def configure_player() -> dict:
    config = _get_configuration(PLAYER_CONFIG_PATH)
    config["bullet"]["color"] = get_color(config["bullet"], "color")
    return config


def configure_enemies() -> dict:
    return _get_configuration(ENEMIES_CONFIG_PATH)