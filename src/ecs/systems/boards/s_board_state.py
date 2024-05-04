from pygame import Vector2
from esper import World
from src.ecs.components.base import CTransform
from src.ecs.components.states import CBoardState, BoardState
from src.ecs.components.tags import CTagBoard


def system_board_state(world: World):
    components = world.get_components(CTagBoard, CBoardState, CTransform)

    c_tag: CTagBoard
    c_h_state: CBoardState
    c_transform: CTransform
    for entity, (c_tag, c_h_state, c_transform) in components:
        if c_h_state.state == BoardState.IDLE:
            _do_idle_state(world, entity, c_tag, c_transform)
        elif c_h_state.state == BoardState.LOADING:
            _do_loading_state(c_tag, c_h_state, c_transform)


def _do_idle_state(world: World, entity: int, tag: CTagBoard, transform: CTransform):
    pass


def _do_loading_state(tag: CTagBoard, state: CBoardState, transform: CTransform):
    pos_fin = Vector2(*tag.pos_fin)
    if transform.pos.distance_to(pos_fin) <= tag.minimum_distance:
        state.state = BoardState.IDLE
        transform.pos.x = tag.pos_fin[0]
        transform.pos.y = tag.pos_fin[1]
