from rl_chess.domain.board.ChessBoard import ChessBoard
from rl_chess.enums.Enums import Color
from rl_chess.service.PieceMovementService import PieceMovementService


class PathBlockSimulation:

    @staticmethod
    def run():
        chess_board = ChessBoard()
        chess_board.move_piece(0, 0, 1, 3)
        chess_board.move_piece(7, 5, 3, 3)
        chess_board.render()

        piece_movement_service = PieceMovementService()
        possible_moves = piece_movement_service.get_possible_moves_for_all_pieces_that_can_move(Color.BLACK, chess_board)['B_Ro_0']
        print(possible_moves)
