from typing import TYPE_CHECKING, Optional

from settings import SETTINGS

if TYPE_CHECKING:
    from network.connection_manager import NetworkManager
    from ui.assets import AssetManager
    from ui.screen_manager import ScreenManager


class ServiceContainer:
    def __init__(self):
        self._asset_manager: Optional['AssetManager'] = None
        self._network_manager: Optional['NetworkManager'] = None
        self._screen_manager: Optional['ScreenManager'] = None
    
    def initialize_assets(self) -> 'AssetManager':
        if self._asset_manager is None:
            from ui.assets import AssetManager
            self._asset_manager = AssetManager()
        return self._asset_manager
    
    def initialize_network(self) -> 'NetworkManager':
        if self._network_manager is None:
            from network.connection_manager import NetworkManager
            self._network_manager = NetworkManager()
        return self._network_manager
    
    def initialize_screen_manager(
        self,
        width: int,
        height: int,
        decorated: bool = True
    ) -> 'ScreenManager':
        if self._screen_manager is None:
            from ui.screen_manager import ScreenManager
            self._screen_manager = ScreenManager(width, height, decorated)
        return self._screen_manager
    
    @property
    def asset_manager(self) -> 'AssetManager':
        if self._asset_manager is None:
            raise RuntimeError("AssetManager not initialized. Call initialize_assets() first.")
        return self._asset_manager
    
    @property
    def network_manager(self) -> 'NetworkManager':
        if self._network_manager is None:
            raise RuntimeError("NetworkManager not initialized. Call initialize_network() first.")
        return self._network_manager
    
    @property
    def screen_manager(self) -> 'ScreenManager':
        if self._screen_manager is None:
            raise RuntimeError("ScreenManager not initialized. Call initialize_screen_manager() first.")
        return self._screen_manager
