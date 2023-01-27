from rl_chess.domain.pieces.Piece import Piece
from rl_chess.enums.Enums import MoveDirection, Color


class Queen(Piece):
    move_directions = [MoveDirection.UP, MoveDirection.DOWN, MoveDirection.LEFT, MoveDirection.RIGHT,
                       MoveDirection.UP_LEFT, MoveDirection.UP_RIGHT, MoveDirection.DOWN_LEFT, MoveDirection.DOWN_RIGHT]

    move_range = 8

    def __init__(self, pos_y: int, pos_x: int, color: Color, alive=True):
        super().__init__(
            pos_y=pos_y,
            pos_x=pos_x,
            color=color,
            short_name="Qu_0",
            alive=alive
        )
