from typing import List, Optional

import pygame

from settings import SETTINGS
from ui.assets import AssetManager
from ui.screen import Screen
from ui.screens.game import GameScreen


class PauseScreen(Screen):
    def __init__(
        self,
        game_screen: GameScreen,
        assets: Optional[AssetManager] = None,
    ) -> None:
        super().__init__(assets)
        self.game_screen = game_screen

    def handle_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        for event in events:
            if event.type == pygame.QUIT:
                return SETTINGS.SCREEN_NAMES.QUIT
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                self.game_screen.session.resume()
                return SETTINGS.SCREEN_NAMES.GAME
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.game_screen.session.resume()
                return SETTINGS.SCREEN_NAMES.GAME
            if event.key == pygame.K_q:
                self.game_screen.session.reset()
                return SETTINGS.SCREEN_NAMES.MENU
        return None

    def update(self, delta_time: float) -> Optional[str]:
        return None

    def render(self, surface: pygame.Surface) -> None:
        self.game_screen.render(surface)
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        self._draw_text(
            surface,
            "PAUSE",
            SETTINGS.UI_TYPOGRAPHY.DISPLAY,
            SETTINGS.UI_THEME.TEXT_PRIMARY,
            (surface.get_width() // 2, 250),
        )
        self._draw_text(
            surface,
            "ENTER para voltar",
            SETTINGS.UI_TYPOGRAPHY.BODY,
            SETTINGS.UI_THEME.YELLOW,
            (surface.get_width() // 2, 315),
        )
