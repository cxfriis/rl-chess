from rl_chess.domain.pieces import Piece


class Tile:

    def __init__(self, pos_y: int, pos_x: int, occupant: Piece = None):
        self.coords = pos_y, pos_x
        self.occupant = occupant

    def add_occupant(self, occupant: Piece) -> None:
        self.occupant = occupant

    def remove_occupant(self) -> None:
        self.occupant = None

    def is_occupied(self) -> bool:
        return self.occupant is not None

    def __str__(self):
        return "      " if not self.occupant else self.occupant.get_id()
