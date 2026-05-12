from typing import List, Optional

import pygame

from engine import GameController, GameSession, GameState, Tile
from settings import SETTINGS
from ui.assets import AssetManager
from ui.screen import Screen


class GameScreen(Screen):
    def __init__(
        self,
        game_controller: GameController,
        session: GameSession,
        assets: Optional[AssetManager] = None,
    ) -> None:
        super().__init__(assets)
        self.game_controller = game_controller
        self.session = session

    def handle_events(self, events: List[pygame.event.Event]) -> Optional[str]:
        for event in events:
            if event.type == pygame.QUIT:
                return SETTINGS.SCREEN_NAMES.QUIT
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_ESCAPE:
                self.session.pause()
                return SETTINGS.SCREEN_NAMES.PAUSE
            if self.session.state != GameState.RUNNING:
                continue
            if event.key == pygame.K_LEFT:
                self.game_controller.move_left()
            elif event.key == pygame.K_RIGHT:
                self.game_controller.move_right()
            elif event.key == pygame.K_DOWN:
                self.game_controller.move_down()
            elif event.key == pygame.K_UP:
                self.game_controller.rotate()
            elif event.key == pygame.K_SPACE:
                self.game_controller.hard_drop()
        return None

    def update(self, delta_time: float) -> Optional[str]:
        if self.session.state == GameState.GAME_OVER:
            return SETTINGS.SCREEN_NAMES.GAME_OVER
        
        if self.session.state == GameState.RUNNING:
            self.game_controller.update(delta_time)
        
        return None

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(SETTINGS.UI_THEME.BG_DARKER)
        self._draw_board(surface)
        self._draw_active_piece(surface)
        self._draw_hud(surface)

    def _draw_board(self, surface: pygame.Surface) -> None:
        tile_size = SETTINGS.GRID.TILE_SIZE
        board_rect = pygame.Rect(
            0,
            0,
            SETTINGS.GRID.GAME_WIDTH,
            SETTINGS.GRID.GAME_HEIGHT,
        )
        pygame.draw.rect(surface, SETTINGS.UI_THEME.BG_DARK, board_rect)

        for y, row in enumerate(self.game_controller.board.grid):
            for x, tile in enumerate(row):
                self._draw_tile(surface, tile, x, y)

        for x in range(SETTINGS.GRID.GRID_WIDTH + 1):
            pygame.draw.line(
                surface,
                SETTINGS.UI_THEME.BG_MEDIUM,
                (x * tile_size, 0),
                (x * tile_size, SETTINGS.GRID.GAME_HEIGHT),
            )
        for y in range(SETTINGS.GRID.GRID_HEIGHT + 1):
            pygame.draw.line(
                surface,
                SETTINGS.UI_THEME.BG_MEDIUM,
                (0, y * tile_size),
                (SETTINGS.GRID.GAME_WIDTH, y * tile_size),
            )

    def _draw_active_piece(self, surface: pygame.Surface) -> None:
        piece = self.game_controller.current_piece
        if piece is None:
            return

        for x, y in piece.get_occupied_places():
            self._draw_tile(surface, piece.tile, x, y)

    def _draw_tile(self, surface: pygame.Surface, tile: Tile, x: int, y: int) -> None:
        if tile == Tile.EMPTY:
            return

        tile_size = SETTINGS.GRID.TILE_SIZE
        rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)

        if self.assets is not None:
            try:
                surface.blit(self.assets.get_tile_surface(tile), rect)
                return
            except (KeyError, FileNotFoundError, pygame.error):
                pass

        color = SETTINGS.TILE_COLORS.get_tile_info(tile).color
        pygame.draw.rect(surface, color, rect.inflate(-2, -2), border_radius=3)

    def _draw_hud(self, surface: pygame.Surface) -> None:
        left = SETTINGS.GRID.GAME_WIDTH + 24
        self._draw_text(surface, "SCORE", SETTINGS.UI_TYPOGRAPHY.BODY, SETTINGS.UI_THEME.TEXT_MUTED, (left + 76, 70))
        self._draw_text(surface, str(self.session.score), SETTINGS.UI_TYPOGRAPHY.LARGE, SETTINGS.UI_THEME.TEXT_PRIMARY, (left + 76, 105))
        self._draw_text(surface, "LEVEL", SETTINGS.UI_TYPOGRAPHY.BODY, SETTINGS.UI_THEME.TEXT_MUTED, (left + 76, 170))
        self._draw_text(surface, str(self.session.level), SETTINGS.UI_TYPOGRAPHY.LARGE, SETTINGS.UI_THEME.TEXT_PRIMARY, (left + 76, 205))
        self._draw_text(surface, "LINES", SETTINGS.UI_TYPOGRAPHY.BODY, SETTINGS.UI_THEME.TEXT_MUTED, (left + 76, 270))
        self._draw_text(surface, str(self.session.total_lines), SETTINGS.UI_TYPOGRAPHY.LARGE, SETTINGS.UI_THEME.TEXT_PRIMARY, (left + 76, 305))
