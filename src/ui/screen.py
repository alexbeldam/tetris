from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, TYPE_CHECKING

import pygame

from settings import SETTINGS
from ui.assets import AssetManager

if TYPE_CHECKING:
    from ui.audio import AudioManager


Color = Tuple[int, int, int]


class Screen(ABC):
    def __init__(self, assets: Optional[AssetManager] = None, audio_manager: Optional["AudioManager"] = None) -> None:
        self.assets = assets
        self.audio_manager = audio_manager

    @abstractmethod
    def handle_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        """Process input and optionally return the next screen name."""

    @abstractmethod
    def update(self, delta_time: float) -> Optional[str]:
        """Update screen-specific logic and optionally return the next screen name."""

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Draw the screen."""

    def _font(self, size: int) -> pygame.font.Font:
        if self.assets is not None:
            try:
                return self.assets.get_font(size)
            except (KeyError, FileNotFoundError, pygame.error):
                pass
        return pygame.font.Font(None, size)

    def _draw_text(
        self,
        surface: pygame.Surface,
        text: str,
        size: int,
        color: Color,
        center: Tuple[int, int],
    ) -> None:
        rendered = self._font(size).render(text, True, color)
        surface.blit(rendered, rendered.get_rect(center=center))
    
    def _try_load_image(self, image_name: str) -> Optional[pygame.Surface]:
        if self.assets is not None:
            try:
                return self.assets.get_image(image_name)
            except (KeyError, FileNotFoundError, pygame.error):
                pass
        return None
