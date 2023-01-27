from rl_chess.domain.pieces.Piece import Piece
from rl_chess.enums.Enums import MoveDirection, Color


class Pawn(Piece):
    move_directions = [MoveDirection.UP, MoveDirection.DOWN, MoveDirection.UP_LEFT, MoveDirection.UP_RIGHT,
                       MoveDirection.DOWN_LEFT, MoveDirection.DOWN_RIGHT]

    move_range = 1
    move_range_2 = 2

    def __init__(self, pos_y: int, pos_x: int, color: Color, alive=True):
        super().__init__(
            pos_y=pos_y,
            pos_x=pos_x,
            color=color,
            short_name=f"Pa_{pos_x}",
            alive=alive
        )

    @staticmethod
    def get_moves_for_color(color: Color):
        if color == Color.WHITE:
            return [MoveDirection.UP, MoveDirection.UP_LEFT, MoveDirection.UP_RIGHT]
        else:
            return [MoveDirection.DOWN, MoveDirection.DOWN_LEFT, MoveDirection.DOWN_RIGHT]
