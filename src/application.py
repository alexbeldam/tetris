import pygame

from game_initializer import GameInitializer
from service_container import ServiceContainer
from settings import SETTINGS
from ui.screen_factory import ScreenFactory
import utils.env_manager as env
from utils.logger import log


class Application:
    def __init__(self):
        self.services = ServiceContainer()
        self.game_initializer: GameInitializer = None
        self.initialized = False
    
    def run(self) -> None:
        try:
            self._load_environment()
            self._initialize_pygame()
            self._initialize_services()
            self._initialize_game()
            self._initialize_screens()
            
            log.info("🚀 Application initialized successfully - starting game")
            
            log.debug(f"Switching to initial screen: {SETTINGS.SCREEN_NAMES.LOADING}")
            self.services.screen_manager.switch_to(SETTINGS.SCREEN_NAMES.LOADING)
            
            if self.services.screen_manager.current_screen:
                self.services.screen_manager.current_screen.render(self.services.screen_manager.surface)
                pygame.display.flip()
            
            self.services.screen_manager.run()
            
        finally:
            self._cleanup()
    
    def _load_environment(self) -> None:
        env.load_env_vars()
        log.debug("📋 Environment configuration loaded from .env file")
    
    def _initialize_pygame(self) -> None:
        pygame.init()
        log.debug(f"🎮 Pygame {pygame.version.ver} initialized successfully")
    
    def _initialize_services(self) -> None:
        splash_size = SETTINGS.GRID.TILE_SIZE * SETTINGS.LOADING_LAYOUT.SPLASH_SIZE_MULTIPLIER
        log.debug(f"🖥️  Creating splash screen ({splash_size}x{splash_size}, borderless)")
        self.services.initialize_screen_manager(
            width=splash_size,
            height=splash_size,
            decorated=False
        )
        
        log.debug("📦 Initializing asset manager for game resources")
        self.services.initialize_assets()
        
        log.debug("� Initializing audio manager for music and sound effects")
        self.services.initialize_audio()
        
        log.debug("�🌐 Establishing database connection for leaderboard data")
        net = self.services.initialize_network()
        
        if not net.wait_for_connection(timeout=SETTINGS.NETWORK.CONNECTION_TIMEOUT):
            log.warning(f"⚠️  Database connection timeout after {SETTINGS.NETWORK.CONNECTION_TIMEOUT}s - running in offline mode (leaderboard unavailable)")
    
    def _initialize_game(self) -> None:
        self.game_initializer = GameInitializer(self.services)
        game_controller, game_session = self.game_initializer.initialize()
        
        self.game_controller = game_controller
        self.game_session = game_session
        self.initialized = True
    
    def _initialize_screens(self) -> None:
        screens = ScreenFactory.create_all_screens(
            self.game_controller,
            self.game_session,
            self.services
        )
        
        ScreenFactory.register_screens(self.services.screen_manager, screens)
    
    def _cleanup(self) -> None:
        log.debug("🔌 Shutting down application and releasing resources")
        pygame.quit()
        log.info("👋 Application closed successfully")
