import json

from .prefab_base import get_color

WINDOW_CONFIG_PATH = "assets/cfg/window.json"
INTERFACE_CONFIG_PATH = "assets/cfg/interface.json"
INTRO_TEXT_CONFIG_PATH = "assets/cfg/intro_text.json"
BOARD_TEXT_CONFIG_PATH = "assets/cfg/board_text.json"
PAUSED_TEXT_CONFIG_PATH = "assets/cfg/paused_text.json"
GAME_END_CONFIG_PATH = "assets/cfg/game_end.json"
STARFIELD_CONFIG_PATH = "assets/cfg/starfield.json"
LEVELS_CONFIG_PATH = "assets/cfg/levels.json"
PLAYER_CONFIG_PATH = "assets/cfg/player.json"
ENEMIES_CONFIG_PATH = "assets/cfg/enemies.json"
DEATH_CONFIG_PATH = "assets/cfg/death_config.json"
LIVES_CONFIG_PATH = "assets/cfg/lives_config.json"


def _get_configuration(path: str) -> dict:
    config: dict
    with open(path) as f:
        config = json.load(f)
    return config


def configure_window() -> dict:
    return _get_configuration(WINDOW_CONFIG_PATH)


def configure_interface() -> dict:
    return _get_configuration(INTERFACE_CONFIG_PATH)


def _transform_text_data(text: dict, interface: dict):
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
    for text in config["texts"]:
        _transform_text_data(text, interface)
    _transform_image_data(config)
    return config


def configure_board_text(interface: dict) -> dict:
    config: dict = _get_configuration(BOARD_TEXT_CONFIG_PATH)
    for text in config["texts"]:
        _transform_text_data(text, interface)
    return config


def configure_paused_text(interface: dict) -> dict:
    config: dict = _get_configuration(PAUSED_TEXT_CONFIG_PATH)
    _transform_text_data(config["text"], interface)
    return config


def configure_game_end(interface: dict) -> dict:
    config: dict = _get_configuration(GAME_END_CONFIG_PATH)
    _transform_text_data(config["GAME_OVER"]["text"], interface)
    _transform_text_data(config["GAME_WON"]["text"], interface)
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
            invader["start_position"] = (
                invader["start_position"]["x"],
                invader["start_position"]["y"],
            )
            invader["attack_velocity"] = (
                invader["attack_velocity"]["x"],
                invader["attack_velocity"]["y"],
            )
            invader["move_velocity"] = (
                invader["move_velocity"]["x"],
                invader["move_velocity"]["y"],
            )
            invader["return_velocity"] = (
                invader["return_velocity"]["x"],
                invader["return_velocity"]["y"],
            )
    return config


def configure_player() -> dict:
    config = _get_configuration(PLAYER_CONFIG_PATH)
    config["bullet"]["color"] = get_color(config["bullet"], "color")
    return config


def configure_enemies() -> dict:
    return _get_configuration(ENEMIES_CONFIG_PATH)

def configure_death() -> dict:
    return _get_configuration(DEATH_CONFIG_PATH)

def configure_lives() -> dict:
    return _get_configuration(LIVES_CONFIG_PATH)