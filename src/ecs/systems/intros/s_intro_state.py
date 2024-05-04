from pygame import Vector2
from esper import World
from src.ecs.components.base import CTransform
from src.ecs.components.states import CIntroState, IntroState
from src.ecs.components.tags import CTagIntro


def system_intro_state(world: World, show_intro: bool):
    components = world.get_components(CTagIntro, CIntroState, CTransform)

    c_tag: CTagIntro
    c_h_state: CIntroState
    c_transform: CTransform
    for entity, (c_tag, c_h_state, c_transform) in components:
        if c_h_state.state == IntroState.IDLE:
            _do_idle_state(world, entity, c_tag, c_transform, show_intro)
        elif c_h_state.state == IntroState.LOADING:
            _do_loading_state(c_tag, c_h_state, c_transform)


def _do_idle_state(
    world: World, entity: int, tag: CTagIntro, transform: CTransform, show_intro: bool
):
    pos_fin = Vector2(*tag.pos_fin)
    if not show_intro and transform.pos.distance_to(pos_fin) == 0:
        world.delete_entity(entity)


def _do_loading_state(tag: CTagIntro, state: CIntroState, transform: CTransform):
    pos_fin = Vector2(*tag.pos_fin)
    if transform.pos.distance_to(pos_fin) <= tag.minimum_distance:
        state.state = IntroState.IDLE
        transform.pos.x = tag.pos_fin[0]
        transform.pos.y = tag.pos_fin[1]
