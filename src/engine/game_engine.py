import asyncio

import pygame

import esper
from src.create.prefab_config import (
    configure_board_text,
    configure_interface,
    configure_intro_text,
    configure_starfield,
    configure_window,
)
from src.create.components import create_intro_inputs
from src.create.prefab_interface import (
    get_screen_color,
    set_caption,
    set_screen,
)
from src.create.components import (
    create_intro_image,
    create_intro_text,
    create_board_text,
)
from src.ecs.components.base import CInput, InputPhase
from src.ecs.systems.base import system_input, system_rendering
from src.ecs.systems.boards import system_board_movement, system_board_state
from src.ecs.systems.intros import system_intro_movement, system_intro_state
from src.ecs.systems.stars import (
    system_star_screen_bounce,
    system_star_movement,
    system_star_state,
    sytem_star_spawner,
)


class GameEngine:
    def __init__(self) -> None:
        # Configuracion archivos
        self.window_cfg: dict = configure_window()
        self.interface: dict = configure_interface()
        self.intro_text: dict = configure_intro_text(self.interface)
        self.board_text: dict = configure_board_text(self.interface)
        self.starfield_cfg: dict = configure_starfield()

        # Configuracion base
        self.framerate = self.window_cfg["framerate"]
        self.is_running = False
        self.delta_time = 0.0

        self.show_intro = True

        pygame.init()
        self.clock = pygame.time.Clock()
        self.ecs_world = esper.World()

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self.screen = set_screen(self.window_cfg)
        self.screen_rgb = get_screen_color(self.window_cfg)
        set_caption(self.window_cfg)

        for text in self.intro_text["texts"]:
            create_intro_text(self.ecs_world, text)
        for img in self.intro_text["images"]:
            create_intro_image(self.ecs_world, img)
        for text in self.board_text["texts"]:
            create_board_text(self.ecs_world, text)

        create_intro_inputs(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        sytem_star_spawner(self.ecs_world, self.starfield_cfg, self.window_cfg)
        system_intro_movement(self.ecs_world, self.delta_time)
        system_board_movement(self.ecs_world, self.delta_time)
        system_star_movement(self.ecs_world, self.delta_time)

        system_intro_state(self.ecs_world, self.show_intro)
        system_board_state(self.ecs_world)
        system_star_state(self.ecs_world, self.delta_time)

        system_star_screen_bounce(self.ecs_world, self.screen)

        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.screen_rgb)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

    def _do_action(self, c_input: CInput, event: pygame.event.Event = None):
        if c_input.name == "PLAYER_Z":
            self.show_intro = False
