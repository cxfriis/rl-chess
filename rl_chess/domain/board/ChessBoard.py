from rl_chess.domain.board.Tile import Tile
from rl_chess.domain.pieces.Bishop import Bishop
from rl_chess.domain.pieces.King import King
from rl_chess.domain.pieces.Knight import Knight
from rl_chess.domain.pieces.Pawn import Pawn
from rl_chess.domain.pieces.Piece import Piece
from rl_chess.domain.pieces.Queen import Queen
from rl_chess.domain.pieces.Rook import Rook
from rl_chess.enums.Enums import Color
import numpy as np


class ChessBoard:

    def __init__(self):
        self.grid = [[Tile(0, 0), Tile(0, 1), Tile(0, 2), Tile(0, 3), Tile(0, 4), Tile(0, 5), Tile(0, 6), Tile(0, 7)],
                     [Tile(1, 0), Tile(1, 1), Tile(1, 2), Tile(1, 3), Tile(1, 4), Tile(1, 5), Tile(1, 6), Tile(1, 7)],
                     [Tile(2, 0), Tile(2, 1), Tile(2, 2), Tile(2, 3), Tile(2, 4), Tile(2, 5), Tile(2, 6), Tile(2, 7)],
                     [Tile(3, 0), Tile(3, 1), Tile(3, 2), Tile(3, 3), Tile(3, 4), Tile(3, 5), Tile(3, 6), Tile(3, 7)],
                     [Tile(4, 0), Tile(4, 1), Tile(4, 2), Tile(4, 3), Tile(4, 4), Tile(4, 5), Tile(4, 6), Tile(4, 7)],
                     [Tile(5, 0), Tile(5, 1), Tile(5, 2), Tile(5, 3), Tile(5, 4), Tile(5, 5), Tile(5, 6), Tile(5, 7)],
                     [Tile(6, 0), Tile(6, 1), Tile(6, 2), Tile(6, 3), Tile(6, 4), Tile(6, 5), Tile(6, 6), Tile(6, 7)],
                     [Tile(7, 0), Tile(7, 1), Tile(7, 2), Tile(7, 3), Tile(7, 4), Tile(7, 5), Tile(7, 6), Tile(7, 7)]]

        self.white_pieces = {}
        self.black_pieces = {}
        self.reset()

    def get_tile(self, pos_y: int, pos_x: int) -> Tile:
        return self.grid[pos_y][pos_x]

    def add_occupant(self, occupant: Piece) -> None:
        self.grid[occupant.coords[0]][occupant.coords[1]].add_occupant(occupant)
        if occupant.color == Color.WHITE:
            self.white_pieces[occupant.get_id()] = occupant
        else:
            self.black_pieces[occupant.get_id()] = occupant

    def remove_occupant_from_tile(self, pos_y: int, pos_x: int) -> None:
        self.get_tile(pos_y, pos_x).remove_occupant()

    def get_occupant_from_tile(self, pos_y: int, pos_x: int) -> Piece:
        return self.get_tile(pos_y, pos_x).occupant

    def get_occupant_by_id(self, piece_id: str) -> Piece:
        white_piece = self.white_pieces.get(piece_id)
        return white_piece if white_piece is not None else self.black_pieces.get(piece_id)

    def clear(self) -> None:
        for row_index in range(8):
            for column_index in range(8):
                occupant = self.get_occupant_from_tile(row_index, column_index)
                if occupant is not None:
                    occupant.alive = False
                self.remove_occupant_from_tile(row_index, column_index)
        self.white_pieces.clear()
        self.black_pieces.clear()

    def reset(self) -> None:
        self.clear()

        self.add_occupant(Rook(7, 0, Color.WHITE))
        self.add_occupant(Knight(7, 1, Color.WHITE))
        self.add_occupant(Bishop(7, 2, Color.WHITE))
        self.add_occupant(Queen(7, 3, Color.WHITE))
        self.add_occupant(King(7, 4, Color.WHITE))
        self.add_occupant(Bishop(7, 5, Color.WHITE))
        self.add_occupant(Knight(7, 6, Color.WHITE))
        self.add_occupant(Rook(7, 7, Color.WHITE))

        self.add_occupant(Pawn(6, 0, Color.WHITE))
        self.add_occupant(Pawn(6, 1, Color.WHITE))
        self.add_occupant(Pawn(6, 2, Color.WHITE))
        self.add_occupant(Pawn(6, 3, Color.WHITE))
        self.add_occupant(Pawn(6, 4, Color.WHITE))
        self.add_occupant(Pawn(6, 5, Color.WHITE))
        self.add_occupant(Pawn(6, 6, Color.WHITE))
        self.add_occupant(Pawn(6, 7, Color.WHITE))

        self.add_occupant(Pawn(1, 0, Color.BLACK))
        self.add_occupant(Pawn(1, 1, Color.BLACK))
        self.add_occupant(Pawn(1, 2, Color.BLACK))
        self.add_occupant(Pawn(1, 3, Color.BLACK))
        self.add_occupant(Pawn(1, 4, Color.BLACK))
        self.add_occupant(Pawn(1, 5, Color.BLACK))
        self.add_occupant(Pawn(1, 6, Color.BLACK))
        self.add_occupant(Pawn(1, 7, Color.BLACK))

        self.add_occupant(Rook(0, 0, Color.BLACK))
        self.add_occupant(Knight(0, 1, Color.BLACK))
        self.add_occupant(Bishop(0, 2, Color.BLACK))
        self.add_occupant(Queen(0, 3, Color.BLACK))
        self.add_occupant(King(0, 4, Color.BLACK))
        self.add_occupant(Bishop(0, 5, Color.BLACK))
        self.add_occupant(Knight(0, 6, Color.BLACK))
        self.add_occupant(Rook(0, 7, Color.BLACK))

    def is_tile_occupied(self, pos_y: int, pos_x: int) -> bool:
        return self.get_tile(pos_y, pos_x).is_occupied()

    def move_piece(self, pos_y: int, pos_x: int, destination_y: int, destination_x: int):
        # Checks need to be performed before calling this function to determine if move is legit

        if self.is_tile_occupied(pos_y, pos_x):
            piece = self.get_occupant_from_tile(pos_y, pos_x)
            tile = self.get_tile(pos_y, pos_x)
            tile.remove_occupant()

            destination_occupant = self.get_occupant_from_tile(destination_y, destination_x)
            if destination_occupant is not None:
                destination_occupant.alive = False
            destination_tile = self.get_tile(destination_y, destination_x)

            piece.coords = destination_y, destination_x
            destination_tile.add_occupant(piece)

    def render(self) -> None:
        print("-------------------------------------------------------------------")
        row_index = 0
        for row in self.grid:
            line = f"{row_index}.| "
            for tile in row:
                line += str(tile)
                line += "| "
            print(line, "\n--|-------|-------|-------|-------|-------|-------|-------|-------|")
            row_index += 1
        line = "   "
        for column_index in range(8):
            line += f"   {column_index}.   "
        print(line)
        print("-------------------------------------------------------------------")

    def get_white_pieces(self) -> {}:
        white_pieces = {}
        for pos_y in range(8):
            for pos_x in range(8):
                piece = self.get_occupant_from_tile(pos_y, pos_x)
                if piece is not None and piece.color == Color.WHITE:
                    white_pieces[piece.get_id()] = piece

        return white_pieces

    def get_black_pieces(self) -> {}:
        black_pieces = {}
        for pos_y in range(8):
            for pos_x in range(8):
                piece = self.get_occupant_from_tile(pos_y, pos_x)
                if piece is not None and piece.color == Color.BLACK:
                    black_pieces[piece.get_id()] = piece

        return black_pieces
