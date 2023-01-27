from rl_chess.domain.board.ChessBoard import ChessBoard
from rl_chess.domain.pieces.Bishop import Bishop
from rl_chess.domain.pieces.King import King
from rl_chess.domain.pieces.Knight import Knight
from rl_chess.domain.pieces.Pawn import Pawn
from rl_chess.domain.pieces.Piece import Piece
from rl_chess.domain.pieces.Queen import Queen
from rl_chess.domain.pieces.Rook import Rook
from rl_chess.enums.Enums import Color
from rl_chess.service.PawnPromotionService import PawnPromotionService
from rl_chess.service.PieceMovementService import PieceMovementService


class PawnPromotionSimulation:

    @staticmethod
    def run():
        pawn_promotion_service = PawnPromotionService()
        chess_board = ChessBoard()
        chess_board.clear()
        pawn_0 = Pawn(1, 4, Color.BLACK)
        pawn_1 = Pawn(1, 3, Color.BLACK)
        chess_board.add_occupant(pawn_0)
        pawn_promotion_service.promote_to_queen(pawn_0, chess_board)
        chess_board.add_occupant(pawn_1)
        pawn_promotion_service.promote_to_queen(pawn_1, chess_board)
        chess_board.render()

        piece_movement_service = PieceMovementService()
        possible_moves = piece_movement_service.get_possible_moves_for_all_pieces_that_can_move(Color.BLACK, chess_board)
        print(possible_moves)
