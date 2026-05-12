from typing import Tuple

from engine import GameController, GameSession, TetrominoType
from service_container import ServiceContainer
from utils.logger import log


class GameInitializer:
    def __init__(self, services: ServiceContainer):
        self.services = services
        self.game_controller: GameController = None
        self.game_session: GameSession = None
    
    def initialize(self) -> Tuple[GameController, GameSession]:
        log.debug("🎮 Initializing game controller and session")
        
        self.game_controller = GameController()
        self.game_session = GameSession(self.game_controller)
        
        self._setup_event_handlers(self.game_controller)
        
        log.debug(f"Initial game state - Piece: {self.game_controller.current_piece.piece.name if self.game_controller.current_piece else 'None'}, "
                 f"Next: {self.game_controller.next_piece.name if self.game_controller.next_piece else 'None'}, "
                 f"Gravity: {self.game_controller.gravity_interval}s")
        log.debug(f"Session initialized - State: {self.game_session.state.name}, Level: {self.game_session.level}, "
                 f"Score: {self.game_session.score}, Lines: {self.game_session.total_lines}")
        
        return self.game_controller, self.game_session
    
    @staticmethod
    def _setup_event_handlers(game: GameController) -> None:
        def on_line_cleared(lines: int) -> None:
            log.info(f"✨ Cleared {lines} line(s) - checking for level progression")
        
        def on_piece_locked(piece: TetrominoType) -> None:
            log.debug(f"🔒 Piece locked: {piece.name}")
        
        def on_game_over() -> None:
            log.info("💀 Game Over - no more valid moves available")
        
        def on_next_piece(piece: TetrominoType) -> None:
            log.debug(f"🎲 Next piece queued: {piece.name}")
        
        game.on_line_clear(on_line_cleared)
        game.on_piece_locked(on_piece_locked)
        game.on_game_over(on_game_over)
        game.on_next_piece_changed(on_next_piece)
