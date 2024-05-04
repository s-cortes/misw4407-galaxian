from typing import Callable, Optional

from pygame.event import Event
from pygame import KEYDOWN, KEYUP

from esper import World
from src.ecs.components.base import CInput, InputPhase


def system_input(
    world: World, event: Event, do_action: Callable[[CInput, Optional[Event]], None]
):
    print(event)
    components = world.get_component(CInput)
    c_input: CInput
    for _, c_input in components:
        if event.type == KEYDOWN:
            print(f"{c_input.key} - {event.key}")
            if c_input.key == event.key:
                c_input.phase = InputPhase.START
                do_action(c_input)
        elif event.type == KEYUP and c_input.key == event.key:
            c_input.phase = InputPhase.END
            do_action(c_input)
