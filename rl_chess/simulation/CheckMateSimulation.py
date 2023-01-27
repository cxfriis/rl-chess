from rl_chess.domain.board.ChessBoard import ChessBoard
from rl_chess.domain.pieces.Bishop import Bishop
from rl_chess.domain.pieces.King import King
from rl_chess.domain.pieces.Knight import Knight
from rl_chess.domain.pieces.Pawn import Pawn
from rl_chess.domain.pieces.Piece import Piece
from rl_chess.domain.pieces.Queen import Queen
from rl_chess.domain.pieces.Rook import Rook
from rl_chess.enums.Enums import Color
from rl_chess.service.PieceMovementService import PieceMovementService


class CheckMateSimulation:

    @staticmethod
    def run():
        chess_board = ChessBoard()
        chess_board.clear()

        chess_board.add_occupant(King(0, 4, Color.BLACK))
        chess_board.add_occupant(Pawn(1, 4, Color.BLACK))
        chess_board.add_occupant(Pawn(1, 5, Color.BLACK))
        chess_board.add_occupant(Queen(0, 3, Color.BLACK))
        chess_board.add_occupant(Pawn(1, 2, Color.BLACK))
        chess_board.add_occupant(Pawn(1, 1, Color.BLACK))
        chess_board.add_occupant(Queen(4, 0, Color.WHITE))

        chess_board.render()

        piece_movement_service = PieceMovementService()
        possible_moves = piece_movement_service.get_possible_moves_for_all_pieces_that_can_move(Color.BLACK, chess_board)
        print(possible_moves)
