import asyncio

import pygame

import esper
from src.create.components import create_c_level, create_c_player_bullet
from src.create.prefab_config import (
    configure_board_text,
    configure_enemies,
    configure_interface,
    configure_intro_text,
    configure_levels,
    configure_paused_text,
    configure_game_end,
    configure_player,
    configure_starfield,
    configure_window,
    configure_death,
    configure_lives, configure_level_assets,
)
from src.create.components import create_intro_inputs
from src.create.prefab_interface import (
    get_screen_color,
    set_caption,
    set_screen,
)
from src.create.components import create_pause

from src.ecs.components.base import CInput, InputName, InputPhase, CLevel
from src.ecs.components.tags import CTagPlayer
from src.ecs.systems.base import system_input, system_rendering
from src.ecs.systems.base.s_animation import system_animation
from src.ecs.systems.boards import system_board_movement, system_board_state, system_board_update_hi_score
from src.ecs.systems.intros import system_intro_movement, system_intro_state
from src.ecs.systems.invaders.s_invader_bullet_movement import system_invader_bullet_movement
from src.ecs.systems.invaders.s_invaders_attack import system_invaders_attack
from src.ecs.systems.invaders.s_invaders_bullet_spawn import system_update_invaders_bullet_spawner_time, \
    system_invader_bullet_spawner
from src.ecs.systems.invaders.s_invaders_movement import system_invaders_movement
from src.ecs.systems.invaders.s_invaders_oscillation import system_invaders_oscillation
from src.ecs.systems.invaders.s_invaders_spawn import system_update_invaders_spawner_time, system_invader_spawner
from src.ecs.systems.invaders.s_invaders_state import system_invaders_state
from src.ecs.systems.invaders.s_invaders_bullet_collision import system_invader_bullet_collision
from src.ecs.systems.levels import system_level_state
from src.ecs.systems.levels.s_level_assets import system_level_text, system_level_assets
from src.ecs.systems.players import (
    system_player_bullet_movement,
    system_player_bullet_screen_clear,
    system_player_movement,
    system_player_screen_bounce,
    system_player_bullet_collision,
    system_player_lives,
)
from src.ecs.systems.players.s_player_invader_collision import system_player_invader_collision
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
        self.interface_cfg: dict = configure_interface()
        self.intro_cfg: dict = configure_intro_text(self.interface_cfg)
        self.board_cfg: dict = configure_board_text(self.interface_cfg)
        self.pause_cfg: dict = configure_paused_text(self.interface_cfg)
        self.game_end_cfg: dict = configure_game_end(self.interface_cfg)

        self.starfield_cfg: dict = configure_starfield()
        self.enemies_cfg: dict = configure_enemies()
        self.levels_cfg: dict = configure_levels()
        self.player_cfg: dict = configure_player()
        self.death_cfg: dict = configure_death()
        self.lives_cfg: dict = configure_lives()
        self.level_assets: dict = configure_level_assets()

        # Configuracion base
        self.framerate = self.window_cfg["framerate"]
        self.is_running = False
        self.delta_time = 0.0

        self.level_id: int = None
        self.pause_text_id: int

        pygame.init()
        self.clock = pygame.time.Clock()
        self.ecs_world = esper.World()

    @property
    def player_id(self) -> int:
        return self.level.player

    @property
    def level(self) -> CLevel:
        return (
            self.ecs_world.component_for_entity(self.level_id, CLevel)
            if self.level_id is not None
            else None
        )

    @property
    def player_tag(self) -> CTagPlayer:
        return (
            self.ecs_world.component_for_entity(self.level.player, CTagPlayer)
            if self.level.player is not None
            else None
        )

    @property
    def paused(self) -> bool:
        return self.level.paused

    @property
    def inputs_enabled(self) -> bool:
        return self.level.inputs_enaled

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

        self.level_id = create_c_level(self.ecs_world)
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
        # spawners
        sytem_star_spawner(self.ecs_world, self.starfield_cfg, self.window_cfg)
        system_level_state(
            self.ecs_world,
            self.levels_cfg,
            self.player_cfg,
            self.enemies_cfg,
            self.intro_cfg,
            self.board_cfg,
            self.game_end_cfg,
            self.lives_cfg,
        )
        system_level_assets(self.ecs_world, self.level_assets)

        system_update_invaders_spawner_time(self.ecs_world, self.delta_time)
        system_invader_spawner(self.ecs_world)
        system_update_invaders_bullet_spawner_time(self.ecs_world, self.delta_time)
        system_invader_bullet_spawner(self.ecs_world, self.levels_cfg[self.level.current])

        # movement
        system_intro_movement(self.ecs_world, self.delta_time)
        system_board_movement(self.ecs_world, self.delta_time)
        system_star_movement(self.ecs_world, self.delta_time)

        system_player_movement(self.ecs_world, self.delta_time, self.paused)
        system_invaders_attack(self.ecs_world, self.player_id, self.delta_time, self.level)
        system_invaders_oscillation(self.ecs_world, self.levels_cfg[self.level.current], self.level)
        system_invaders_movement(self.ecs_world, self.delta_time, self.level)

        system_player_bullet_movement(self.ecs_world, self.delta_time, self.paused)
        system_invader_bullet_movement(self.ecs_world, self.delta_time, self.paused)

        # states
        system_intro_state(self.ecs_world, self.level)
        system_board_state(self.ecs_world)
        system_star_state(self.ecs_world, self.delta_time)
        system_invaders_state(self.ecs_world, self.screen)

        # collision
        system_star_screen_bounce(self.ecs_world, self.screen)
        system_player_screen_bounce(self.ecs_world, self.screen)
        system_player_bullet_screen_clear(self.ecs_world, self.player_tag)
        system_invader_bullet_collision(self.ecs_world, self.death_cfg, self.player_tag)
        system_player_bullet_collision(self.ecs_world, self.player_id,
                                      self.levels_cfg[self.level.current], self.death_cfg)
        system_player_invader_collision(self.ecs_world, self.player_id,
                                      self.levels_cfg[self.level.current], self.death_cfg)
        system_player_lives(self.ecs_world, self.player_id)
        system_board_update_hi_score(self.ecs_world)

        # animation
        system_animation(self.ecs_world, self.delta_time)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.screen_rgb)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

    def _do_action(self, c_input: CInput, event: pygame.event.Event = None):
        if not self.inputs_enabled:
            return

        if c_input.name == InputName.PLAYER_P:
            if c_input.phase == InputPhase.START:
                self.level.paused = not self.level.paused

                if self.paused:
                    self.pause_text_id = create_pause(self.ecs_world, self.pause_cfg)
                else:
                    self.ecs_world.delete_entity(self.pause_text_id)
                    self.pause_text_id = None

        if self.paused:
            return

        if c_input.name == InputName.PLAYER_LEFT and self.player_tag:
            if c_input.phase == InputPhase.START:
                self.player_tag.left = True
            elif c_input.phase == InputPhase.END:
                self.player_tag.left = False
        elif c_input.name == InputName.PLAYER_RIGHT and self.player_tag:
            if c_input.phase == InputPhase.START:
                self.player_tag.right = True
            elif c_input.phase == InputPhase.END:
                self.player_tag.right = False

        elif c_input.name == InputName.PLAYER_Z and self.player_tag:
            if c_input.phase == InputPhase.START and self.player_tag.bullets:
                self.player_tag.bullets -= 1
                create_c_player_bullet(self.ecs_world, self.player_id, self.player_cfg)

        elif c_input.name == InputName.PLAYER_Z:
            if c_input.phase == InputPhase.START:
                if self.level.intro_active:
                    self.level.intro_active = False
                elif self.level.completed:
                    self.level.restart = True
