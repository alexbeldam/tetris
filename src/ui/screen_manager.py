from typing import Dict, Optional
import os

import pygame

from settings import SETTINGS
from ui.screen import Screen


class ScreenManager:
    def __init__(self, width: int, height: int, decorated: bool = True) -> None:
        self.clock = pygame.time.Clock()
        self._screens: Dict[str, Screen] = {}
        self.current_screen: Optional[Screen] = None
        self._current_name: Optional[str] = None
        self._running = False
        self._create_window(width, height, decorated)

    def _create_window(self, width: int, height: int, decorated: bool) -> None:
        self._center_window()
        flags = 0 if decorated else pygame.NOFRAME
        self.surface = pygame.display.set_mode((width, height), flags)
        self.surface.fill(SETTINGS.UI_THEME.BG_DARKER)
        pygame.display.flip()

    def _center_window(self) -> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

    def reconfigure_window(
        self,
        width: int,
        height: int,
        caption: str = "",
        icon: Optional[pygame.Surface] = None,
        decorated: bool = True
    ) -> None:
        pygame.display.quit()
        pygame.display.init()
        self._create_window(width, height, decorated)
        
        if caption:
            pygame.display.set_caption(caption)
        
        if icon is not None:
            pygame.display.set_icon(icon)

    def register_screen(self, name: str, screen: Screen) -> None:
        self._screens[name] = screen

    def switch_to(self, name: str) -> None:
        if name not in self._screens:
            raise KeyError(f"Screen '{name}' is not registered.")

        pygame.event.clear()
        self._current_name = name
        self.current_screen = self._screens[name]

    def run(self) -> None:
        if self.current_screen is None:
            raise RuntimeError("Cannot run ScreenManager without an active screen.")

        self._running = True
        while self._running:
            delta_time = self.clock.tick(SETTINGS.DISPLAY.FPS) / 1000.0
            events = pygame.event.get()

            next_screen = self.current_screen.handle_events(events)
            if next_screen == SETTINGS.SCREEN_NAMES.QUIT:
                self._running = False
                break
            if next_screen is not None:
                self.switch_to(next_screen)

            if self.current_screen is None:
                continue

            next_screen = self.current_screen.update(delta_time)
            if next_screen == SETTINGS.SCREEN_NAMES.QUIT:
                self._running = False
                break
            if next_screen is not None:
                self.switch_to(next_screen)
            
            self.current_screen.render(self.surface)
            pygame.display.flip()
    
    def distribute_assets(self, assets) -> None:
        for screen in self._screens.values():
            if hasattr(screen, 'assets'):
                screen.assets = assets
