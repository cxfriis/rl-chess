from rl_chess.domain.pieces.Piece import Piece
from rl_chess.enums.Enums import MoveDirection, Color


class Knight(Piece):
    move_directions = [MoveDirection.ONE_O_CLOCK, MoveDirection.TWO_O_CLOCK, MoveDirection.FOUR_O_CLOCK,
                       MoveDirection.FIVE_O_CLOCK, MoveDirection.SEVEN_O_CLOCK, MoveDirection.EIGHT_O_CLOCK,
                       MoveDirection.TEN_O_CLOCK, MoveDirection.ELEVEN_O_CLOCK]

    move_range = 1

    def __init__(self, pos_y: int, pos_x: int, color: Color, alive=True):
        super().__init__(
            pos_y=pos_y,
            pos_x=pos_x,
            color=color,
            short_name=f"Kn_{0 if pos_x == 1 else 1}",
            alive=alive
        )
