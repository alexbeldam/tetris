from dataclasses import dataclass
from typing import List, Optional, Tuple

from .shapes import Matrix, get_shape
from .tile import Tetromino as TetrominoType, Tile


Position = Tuple[int, int]


@dataclass
class Tetromino:
    piece: TetrominoType
    x: Optional[int] = None
    y: Optional[int] = None
    rotation_index: int = 0

    def __post_init__(self) -> None:
        self.piece = TetrominoType(self.piece)
        self.rotation_index %= 4

        if self.x is None or self.y is None:
            from settings import SETTINGS

            if self.x is None:
                self.x = SETTINGS.TETROMINO.SPAWN_X
            if self.y is None:
                self.y = SETTINGS.TETROMINO.SPAWN_Y

    @property
    def tile(self) -> Tile:
        return self.piece.tile

    @property
    def matrix(self) -> Matrix:
        return get_shape(self.piece, self.rotation_index)

    @property
    def tile_info(self):
        from settings import SETTINGS

        return SETTINGS.TILE_COLORS.get_tile_info(self.tile)

    @property
    def color(self) -> Tuple[int, int, int]:
        return self.tile_info.color

    @property
    def tile_index(self) -> int:
        return self.tile_info.index

    def rotate(self, board: object = None) -> bool:
        next_rotation = (self.rotation_index + 1) % 4
        
        if self.piece == TetrominoType.O:
            self.rotation_index = next_rotation
            return True
        
        kick_offsets = self._get_kick_offsets(self.rotation_index, next_rotation)
        
        for offset_x, offset_y in kick_offsets:
            test_x = self.x + offset_x
            test_y = self.y + offset_y
            
            if not self._would_collide(board, x=test_x, y=test_y, rotation_index=next_rotation):
                self.x = test_x
                self.y = test_y
                self.rotation_index = next_rotation
                return True
        
        return False

    def move_left(self, board: object = None) -> bool:
        return self._move(dx=-1, dy=0, board=board)

    def move_right(self, board: object = None) -> bool:
        return self._move(dx=1, dy=0, board=board)

    def move_down(self, board: object = None) -> bool:
        return self._move(dx=0, dy=1, board=board)

    def fall(self, board: object = None) -> int:
        distance = 0

        while self.move_down(board):
            distance += 1
            if board is None:
                break

        return distance

    def get_occupied_places(self) -> List[Position]:
        return [
            (self.x + col_index, self.y + row_index)
            for row_index, row in enumerate(self.matrix)
            for col_index, cell in enumerate(row)
            if cell
        ]

    def _move(self, dx: int, dy: int, board: object = None) -> bool:
        next_x = self.x + dx
        next_y = self.y + dy

        if self._would_collide(board, x=next_x, y=next_y):
            return False

        self.x = next_x
        self.y = next_y
        return True

    def _would_collide(
        self,
        board: object = None,
        *,
        x: Optional[int] = None,
        y: Optional[int] = None,
        rotation_index: Optional[int] = None,
    ) -> bool:
        if board is None:
            return False

        target_x = self.x if x is None else x
        target_y = self.y if y is None else y
        target_rotation = (
            self.rotation_index if rotation_index is None else rotation_index
        )

        return board.check_collision(
            get_shape(self.piece, target_rotation),
            target_x,
            target_y,
        )
    
    def _get_kick_offsets(self, from_rotation: int, to_rotation: int) -> List[Tuple[int, int]]:
        from settings import SETTINGS
        
        rotation_key = f"{from_rotation}->{to_rotation}"
        
        if self.piece == TetrominoType.I:
            return SETTINGS.SRS.I_KICKS.get(rotation_key, [(0, 0)])
        else:
            return SETTINGS.SRS.JLSTZ_KICKS.get(rotation_key, [(0, 0)])