from pygame import Vector2
from esper import World
from src.ecs.components.base import CSurface
from src.ecs.components.states import CStarState, StarState
from src.ecs.components.tags import CTagStar


def system_star_state(world: World, delta_time: int):
    components = world.get_components(CTagStar, CStarState, CSurface)

    c_tag: CTagStar
    c_state: CStarState
    c_surface: CSurface
    for _, (c_tag, c_state, c_surface) in components:
        c_tag.timestamp += delta_time
        if c_state.state == StarState.HIDE:
            _do_hide_state(c_tag, c_state, c_surface)
        elif c_state.state == StarState.SHOW:
            _do_show_state(c_tag, c_state, c_surface)


def _do_hide_state(tag: CTagStar, state: CStarState, surface: CSurface):
    surface.surf.fill(state.colors[state.state.value])
    if tag.timestamp >= tag.blink_rate:
        tag.timestamp = 0
        state.state = StarState.SHOW
    pass

def _do_show_state(tag: CTagStar, state: CStarState, surface: CSurface):
    surface.surf.fill(state.colors[state.state.value])
    if tag.timestamp >= tag.blink_rate:
        tag.timestamp = 0
        state.state = StarState.HIDE

