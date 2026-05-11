class LevelManager:
    def __init__(self) -> None:
        from settings import SETTINGS
        
        self._starting_level: int = SETTINGS.DIFFICULTY.STARTING_LEVEL
        self._lines_per_level: int = SETTINGS.DIFFICULTY.LINES_TO_LEVEL_UP
        self._total_lines: int = 0
    
    @property
    def current_level(self) -> int:
        return self._starting_level + (self._total_lines // self._lines_per_level)
    
    @property
    def total_lines(self) -> int:
        return self._total_lines
    
    @property
    def lines_until_next_level(self) -> int:
        return self._lines_per_level - (self._total_lines % self._lines_per_level)
    
    def add_lines(self, count: int) -> bool:
        if count < 0:
            raise ValueError("Line count cannot be negative")
        
        previous_level: int = self.current_level
        self._total_lines += count
        new_level: int = self.current_level
        
        return new_level > previous_level
    
    def reset(self) -> None:
        self._total_lines = 0
