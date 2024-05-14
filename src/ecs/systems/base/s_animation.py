import esper
from src.ecs.components.base.c_animation import CAnimation
from src.ecs.components.base.c_surface import CSurface


def system_animation(ecs_world: esper.World, delta_time: float):
    components = ecs_world.get_components(CSurface, CAnimation)

    c_s: CSurface
    c_a: CAnimation

    for _, (c_s, c_a) in components:
        c_a.current_time -= delta_time
        if c_a.current_time <= 0:
            c_a.current_time = c_a.animations[c_a.current].framerate
            c_a.current_frame += 1
            if c_a.current_frame > c_a.animations[c_a.current].end:
                c_a.current_frame = c_a.animations[c_a.current].start
            rect_surface = c_s.surf.get_rect()
            c_s.area.width = rect_surface.width / c_a.number_frames
            c_s.area.x = c_s.area.width * c_a.current_frame
