from rl_chess.domain.board.ChessBoard import ChessBoard
from rl_chess.enums.Enums import Color
from rl_chess.service.PieceMovementService import PieceMovementService


class StandardSimulation:

    @staticmethod
    def run():
        chess_board = ChessBoard()
        chess_board.render()

        state = chess_board.get_state()

        piece_movement_service = PieceMovementService()
        piece_movement_service.print_possible_moves_for_all_pieces_of_color(Color.WHITE, chess_board)

        # PLAY GAME
        move_count = 1000
        white_move = True

        for i in range(move_count):
            color = Color.WHITE if white_move else Color.BLACK
            # piece_id, possible_moves = piece_movement_service.get_possible_moves_by_piece_id(color, chess_board)

            piece_id, chosen_move = piece_movement_service.get_random_possible_move_and_id(color, chess_board)

            if piece_id is None:
                print("GAME OVER")
                chess_board.render()
                return

            pos_y, pos_x = chess_board.get_occupant_by_id(piece_id).coords
            destination_y, destination_x = chosen_move

            piece_movement_service.print_move(piece_id, chess_board, pos_y, pos_x, destination_y, destination_x)

            piece = chess_board.get_occupant_by_id(piece_id)
            piece_movement_service.move_piece(piece, chess_board, destination_y, destination_x)

            white_move = not white_move

        chess_board.render()
