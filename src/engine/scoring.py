from typing import Dict


class ScoreCalculator:
    @staticmethod
    def calculate_points(lines_cleared: int, level: int) -> int:
        from settings import SETTINGS
        
        if lines_cleared < 1 or lines_cleared > 4:
            return 0
        
        if level < 1:
            return 0
        
        score_table: Dict[int, int] = SETTINGS.SCORING.SCORE_TABLE
        base_points: int = score_table.get(lines_cleared, 0)
        
        return base_points * level
