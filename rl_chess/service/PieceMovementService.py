import random

from rl_chess.domain.board.ChessBoard import ChessBoard
from rl_chess.domain.pieces.Bishop import Bishop
from rl_chess.domain.pieces.King import King
from rl_chess.domain.pieces.Knight import Knight
from rl_chess.domain.pieces.Pawn import Pawn
from rl_chess.domain.pieces.Piece import Piece
from rl_chess.domain.pieces.Queen import Queen
from rl_chess.domain.pieces.Rook import Rook
from rl_chess.enums.Enums import MoveDirection, Color
from rl_chess.service.PawnPromotionService import PawnPromotionService


class PieceMovementService:

    def move_piece(self, piece: Piece, chess_board: ChessBoard, destination_y: int, destination_x: int):
        chess_board.move_piece(piece.coords[0], piece.coords[1], destination_y, destination_x)

        if PawnPromotionService.is_eligible_for_promotion(piece):
            PawnPromotionService.promote_to_queen(piece, chess_board)

    def get_random_possible_move_and_id(self, color: Color, chess_board: ChessBoard) -> (str, (int, int)):
        possible_moves_by_id = self.get_possible_moves_for_all_pieces_that_can_move(color, chess_board)

        if not possible_moves_by_id:  # no possible moves for player, lead to game over
            return None, {}

        piece_id, possible_moves = random.choice(list(possible_moves_by_id.items()))
        return piece_id, random.choice(possible_moves)

    def get_possible_moves_for_all_pieces_that_can_move(self, color: Color, chess_board: ChessBoard) -> {Piece: [(int, int)]}:
        possible_moves = self.get_possible_moves_for_all_pieces(color, chess_board)
        return {k: v for k, v in possible_moves.items() if len(v) > 0}

    def get_possible_moves_for_all_pieces(self, color: Color, chess_board: ChessBoard) -> {Piece: [(int, int)]}:
        possible_moves = {}
        king_in_check = self.is_king_in_check(color, chess_board)
        pieces_map = chess_board.get_white_pieces() if color == Color.WHITE else chess_board.get_black_pieces()

        for piece_id, piece in pieces_map.items():
            if piece.alive:
                possible_moves[piece_id] = self.get_possible_moves_for_piece(piece, chess_board)
                if king_in_check:  # only perform these steps while in check, else it slows down the game
                    possible_moves[piece_id] = self.filter_out_moves_that_expose_own_king(piece, chess_board, possible_moves[piece_id])

        return possible_moves

    def get_possible_moves_for_piece(self, piece: Piece, chess_board: ChessBoard) -> [(int, int)]:
        if isinstance(piece, King):
            possible_moves = self.get_possible_moves_for_piece_with_actions(piece, chess_board, King.move_directions,
                                                                            King.move_range)

            # King cannot move to positions that will put it in check
            possible_moves = list(filter(lambda move: not self.is_destination_under_threat(piece, chess_board, move[0], move[1]), possible_moves))

        elif isinstance(piece, Queen):
            possible_moves = self.get_possible_moves_for_piece_with_actions(piece, chess_board, Queen.move_directions,
                                                                            Queen.move_range)

        elif isinstance(piece, Bishop):
            possible_moves = self.get_possible_moves_for_piece_with_actions(piece, chess_board, Bishop.move_directions,
                                                                            Bishop.move_range)

        elif isinstance(piece, Knight):
            possible_moves = self.get_possible_moves_for_piece_with_actions(piece, chess_board, Knight.move_directions,
                                                                            Knight.move_range)

        elif isinstance(piece, Rook):
            possible_moves = self.get_possible_moves_for_piece_with_actions(piece, chess_board, Rook.move_directions,
                                                                            Rook.move_range)

        else:  # pawn
            possible_moves = self.get_possible_moves_for_piece_with_actions(piece, chess_board, Pawn.move_directions,
                                                                            Pawn.move_range)

        # filter out any moves that will expose team's King
        if not isinstance(piece, King):
            possible_moves = self.filter_out_moves_that_expose_own_king(piece, chess_board, possible_moves)

        return possible_moves

    def filter_out_moves_that_expose_own_king(self, piece: Piece, chess_board: ChessBoard, moves: [(int, int)]):
        start_pos_y = piece.coords[0]
        start_pos_x = piece.coords[1]
        possible_moves = []

        for move in moves:
            end_pos_y = move[0]
            end_pos_x = move[1]

            # temporarily move piece and see if King becomes vulnerable
            # store destination occupant if one exists
            destination_occupant = chess_board.get_occupant_from_tile(end_pos_y, end_pos_x)
            chess_board.move_piece(start_pos_y, start_pos_x, end_pos_y, end_pos_x)

            if not self.is_king_in_check(piece.color, chess_board):
                possible_moves.append(move)

            chess_board.move_piece(end_pos_y, end_pos_x, start_pos_y, start_pos_x)
            if destination_occupant is not None:
                chess_board.add_occupant(destination_occupant)
                destination_occupant.alive = True

        return possible_moves

    def get_possible_moves_for_piece_with_actions(self, piece: Piece, chess_board: ChessBoard,
                                                  move_directions: [MoveDirection],
                                                  move_range: int) -> [(int, int)]:
        possible_moves = []

        if isinstance(piece, Pawn):
            piece_is_white = piece.color == Color.WHITE

            pos_y = piece.coords[0]
            pos_x = piece.coords[1]

            delta_y_standard = -piece.move_range if piece_is_white else piece.move_range

            forward_move_1 = (pos_y + delta_y_standard, pos_x)
            forward_move_2 = (pos_y + (-piece.move_range_2 if piece_is_white else +piece.move_range_2), pos_x)
            diagonal_move_left = (pos_y + delta_y_standard, pos_x - 1)
            diagonal_move_right = (pos_y + delta_y_standard, pos_x + 1)

            if self.is_coords_in_bounds(forward_move_1[0], forward_move_1[1]) \
                    and not chess_board.is_tile_occupied(forward_move_1[0], forward_move_1[1]):
                possible_moves.append(forward_move_1)

            # no need to check if move is in bounds from starting position
            if ((piece_is_white and pos_y == 6) or (not piece_is_white and pos_y == 1)) \
                    and not chess_board.is_tile_occupied(forward_move_2[0], forward_move_2[1]):
                possible_moves.append(forward_move_2)

            if self.is_coords_in_bounds(diagonal_move_left[0], diagonal_move_left[1]) \
                    and chess_board.is_tile_occupied(diagonal_move_left[0], diagonal_move_left[1]) \
                    and chess_board.get_occupant_from_tile(diagonal_move_left[0], diagonal_move_left[1]).color != piece.color:
                possible_moves.append(diagonal_move_left)

            if self.is_coords_in_bounds(diagonal_move_right[0], diagonal_move_right[1]) \
                    and chess_board.is_tile_occupied(diagonal_move_right[0], diagonal_move_right[1]) \
                    and chess_board.get_occupant_from_tile(diagonal_move_right[0], diagonal_move_right[1]).color != piece.color:
                possible_moves.append(diagonal_move_right)

        else:
            for move_direction in move_directions:
                for range_slice in range(1, move_range + 1):
                    destination_y, destination_x = self.get_destination_coords_by_piece(piece, move_direction, range_slice)

                    if self.is_destination_accessible(piece, chess_board, destination_y, destination_x):
                        possible_moves.append((destination_y, destination_x))

                        if chess_board.is_tile_occupied(destination_y, destination_x):
                            break
                    else:
                        # path is blocked, don't seek any further tiles in this direction
                        break

        if isinstance(piece, King):
            # TODO implement castle move
            pass

        return possible_moves

    @staticmethod
    def get_destination_coords_by_piece(piece: Piece, move_direction: MoveDirection, move_range: int) -> tuple:
        pos_y = piece.coords[0]
        pos_x = piece.coords[1]

        return PieceMovementService.get_destination_coords(pos_y, pos_x, move_direction, move_range)

    @staticmethod
    def get_destination_coords(start_pos_y: int, start_pos_x: int, move_direction: MoveDirection, move_range: int) -> (int, int):
        end_pos_y = start_pos_y
        end_pos_x = start_pos_x

        if move_direction == MoveDirection.UP:
            end_pos_y -= move_range

        elif move_direction == MoveDirection.DOWN:
            end_pos_y += move_range

        elif move_direction == MoveDirection.LEFT:
            end_pos_x -= move_range

        elif move_direction == MoveDirection.RIGHT:
            end_pos_x += move_range

        elif move_direction == MoveDirection.UP_LEFT:
            end_pos_y -= move_range
            end_pos_x -= move_range

        elif move_direction == MoveDirection.UP_RIGHT:
            end_pos_y -= move_range
            end_pos_x += move_range

        elif move_direction == MoveDirection.DOWN_LEFT:
            end_pos_y += move_range
            end_pos_x -= move_range

        elif move_direction == MoveDirection.DOWN_RIGHT:
            end_pos_y += move_range
            end_pos_x += move_range

        elif move_direction == MoveDirection.ONE_O_CLOCK:
            end_pos_y -= 2
            end_pos_x += 1

        elif move_direction == MoveDirection.TWO_O_CLOCK:
            end_pos_y -= 1
            end_pos_x += 2

        elif move_direction == MoveDirection.FOUR_O_CLOCK:
            end_pos_y += 1
            end_pos_x += 2

        elif move_direction == MoveDirection.FIVE_O_CLOCK:
            end_pos_y += 2
            end_pos_x += 1

        elif move_direction == MoveDirection.SEVEN_O_CLOCK:
            end_pos_y += 2
            end_pos_x -= 1

        elif move_direction == MoveDirection.EIGHT_O_CLOCK:
            end_pos_y += 1
            end_pos_x -= 2

        elif move_direction == MoveDirection.TEN_O_CLOCK:
            end_pos_y -= 1
            end_pos_x -= 2

        elif move_direction == MoveDirection.ELEVEN_O_CLOCK:
            end_pos_y -= 2
            end_pos_x -= 1

        return end_pos_y, end_pos_x

    @staticmethod
    def is_coords_in_bounds(pos_y: int, pos_x: int) -> bool:
        return 0 <= pos_y < 8 and 0 <= pos_x < 8

    @staticmethod
    def is_coords_occupied_by_same_color(piece: Piece, chess_board: ChessBoard, destination_y: int, destination_x: int):
        destination_occupant = chess_board.get_occupant_from_tile(destination_y, destination_x)
        return destination_occupant is not None and destination_occupant.color == piece.color

    def is_destination_under_threat(self, piece: Piece, chess_board: ChessBoard, pos_y: int, pos_x: int) -> bool:
        for move_range in range(1, 8):
            destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.UP, move_range)
            destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
            if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
                if destination_occupant is None or destination_occupant.get_id() == piece.get_id():
                    continue
                elif destination_occupant.color != piece.color and (
                        isinstance(destination_occupant, Rook)
                        or isinstance(destination_occupant, Queen)
                        or (move_range == 1 and isinstance(destination_occupant, King))):
                    return True
                else:
                    break  # path is blocked by an occupant so cannot be threatened by any pieces with this move
            else:
                break

        for move_range in range(1, 8):
            destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.DOWN, move_range)
            if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
                destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
                if destination_occupant is None or destination_occupant.get_id() == piece.get_id():
                    continue
                elif destination_occupant.color != piece.color and (
                        isinstance(destination_occupant, Rook)
                        or isinstance(destination_occupant, Queen)
                        or (move_range == 1 and isinstance(destination_occupant, King))):
                    return True
                else:
                    break  # path is blocked by an occupant so cannot be threatened by any pieces with this move
            else:
                break

        for move_range in range(1, 8):
            destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.LEFT, move_range)
            if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
                destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
                if destination_occupant is None or destination_occupant.get_id() == piece.get_id():
                    continue
                elif destination_occupant.color != piece.color and (
                        isinstance(destination_occupant, Rook)
                        or isinstance(destination_occupant, Queen)
                        or (move_range == 1 and isinstance(destination_occupant, King))):
                    return True
                else:
                    break  # path is blocked by an occupant so cannot be threatened by any pieces with this move
            else:
                break

        for move_range in range(1, 8):
            destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.RIGHT, move_range)
            if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
                destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
                if destination_occupant is None or destination_occupant.get_id() == piece.get_id():
                    continue
                elif destination_occupant.color != piece.color and (
                        isinstance(destination_occupant, Rook)
                        or isinstance(destination_occupant, Queen)
                        or (move_range == 1 and isinstance(destination_occupant, King))):
                    return True
                else:
                    break  # path is blocked by an occupant so cannot be threatened by any pieces with this move
            else:
                break

        for move_range in range(1, 8):
            destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.UP_LEFT, move_range)
            if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
                destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
                if destination_occupant is None or destination_occupant.get_id() == piece.get_id():
                    continue
                elif destination_occupant.color != piece.color and (
                        isinstance(destination_occupant, Bishop)
                        or isinstance(destination_occupant, Queen)
                        or (move_range == 1
                            and (isinstance(destination_occupant, King)
                                 or (piece.color == Color.WHITE and isinstance(destination_occupant, Pawn))))):
                    return True
                else:
                    break  # path is blocked by an occupant so cannot be threatened by any pieces with this move
            else:
                break

        for move_range in range(1, 8):
            destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.UP_RIGHT, move_range)
            if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
                destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
                if destination_occupant is None or destination_occupant.get_id() == piece.get_id():
                    continue
                elif destination_occupant.color != piece.color and (
                        isinstance(destination_occupant, Bishop)
                        or isinstance(destination_occupant, Queen)
                        or (move_range == 1
                            and (isinstance(destination_occupant, King)
                                 or (piece.color == Color.WHITE and isinstance(destination_occupant, Pawn))))):
                    return True
                else:
                    break  # path is blocked by an occupant so cannot be threatened by any pieces with this move
            else:
                break

        for move_range in range(1, 8):
            destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.DOWN_LEFT, move_range)
            if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
                destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
                if destination_occupant is None or destination_occupant.get_id() == piece.get_id():
                    continue
                elif destination_occupant.color != piece.color and (
                        isinstance(destination_occupant, Bishop)
                        or isinstance(destination_occupant, Queen)
                        or (move_range == 1
                            and (isinstance(destination_occupant, King)
                                 or (piece.color == Color.BLACK and isinstance(destination_occupant, Pawn))))):
                    return True
                else:
                    break  # path is blocked by an occupant so cannot be threatened by any pieces with this move
            else:
                break

        for move_range in range(1, 8):
            destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.DOWN_RIGHT, move_range)
            if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
                destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
                if destination_occupant is None or destination_occupant.get_id() == piece.get_id():
                    continue
                elif destination_occupant.color != piece.color and (
                        isinstance(destination_occupant, Bishop)
                        or isinstance(destination_occupant, Queen)
                        or (move_range == 1
                            and (isinstance(destination_occupant, King)
                                 or (piece.color == Color.BLACK and isinstance(destination_occupant, Pawn))))):
                    return True
                else:
                    break  # path is blocked by an occupant so cannot be threatened by any pieces with this move
            else:
                break

        destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.ONE_O_CLOCK, 1)
        if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
            destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
            if destination_occupant is not None and destination_occupant.color != piece.color and isinstance(destination_occupant, Knight):
                return True

        destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.TWO_O_CLOCK, 1)
        if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
            destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
            if destination_occupant is not None and destination_occupant.color != piece.color and isinstance(destination_occupant, Knight):
                return True

        destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.FOUR_O_CLOCK, 1)
        if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
            destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
            if destination_occupant is not None and destination_occupant.color != piece.color and isinstance(destination_occupant, Knight):
                return True

        destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.FIVE_O_CLOCK, 1)
        if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
            destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
            if destination_occupant is not None and destination_occupant.color != piece.color and isinstance(destination_occupant, Knight):
                return True

        destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.SEVEN_O_CLOCK, 1)
        if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
            destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
            if destination_occupant is not None and destination_occupant.color != piece.color and isinstance(destination_occupant, Knight):
                return True

        destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.EIGHT_O_CLOCK, 1)
        if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
            destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
            if destination_occupant is not None and destination_occupant.color != piece.color and isinstance(destination_occupant, Knight):
                return True

        destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.TEN_O_CLOCK, 1)
        if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
            destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
            if destination_occupant is not None and destination_occupant.color != piece.color and isinstance(destination_occupant, Knight):
                return True

        destination_coords = PieceMovementService.get_destination_coords(pos_y, pos_x, MoveDirection.ELEVEN_O_CLOCK, 1)
        if self.is_coords_in_bounds(destination_coords[0], destination_coords[1]):
            destination_occupant = chess_board.get_occupant_from_tile(destination_coords[0], destination_coords[1])
            if destination_occupant is not None and destination_occupant.color != piece.color and isinstance(destination_occupant, Knight):
                return True

        return False

    def is_destination_accessible(self, piece: Piece, chess_board: ChessBoard, destination_y: int,
                                  destination_x: int) -> bool:
        """
        Checks if the given piece can move to a destination tile depending on whether it is in bounds and not occupied
        by a piece of the same Color.
        :param piece:
        :param chess_board:
        :param destination_y:
        :param destination_x:
        :return:
        """
        return self.is_coords_in_bounds(destination_y, destination_x) \
               and not self.is_coords_occupied_by_same_color(piece, chess_board, destination_y, destination_x)

    def is_king_in_check(self, color: Color, chess_board: ChessBoard) -> bool:
        king_id = "W_Ki_0" if color == Color.WHITE else "B_Ki_0"
        king = chess_board.get_occupant_by_id(king_id)
        if king:
            king_coords = king.coords
            return self.is_destination_under_threat(king, chess_board, king_coords[0], king_coords[1])
        else:
            # DEBUG - should only happen during a simulation where the player doesn't have a King
            return False

    def print_possible_moves_for_all_pieces_of_color(self, color: Color, chess_board: ChessBoard) -> None:
        print(f"Possible moves for player {color}")

        moves_by_piece_ids = self.get_possible_moves_for_all_pieces(color, chess_board)

        for piece_id, moves in moves_by_piece_ids.items():
            print(f"{piece_id}: {moves}")

    def print_move(self, piece_id: str, chess_board: ChessBoard, pos_y: int, pos_x: int, destination_y: int,
                   destination_x: int) -> None:
        destination_occupant = chess_board.get_occupant_from_tile(destination_y, destination_x)
        if destination_occupant is None:
            print(f"Move {piece_id} from (pos_y={pos_y}, pos_x={pos_x}) to (pos_y={destination_y}, "
                  f"pos_x={destination_x})")
        else:
            print(f"Move {piece_id} from (pos_y={pos_y}, pos_x={pos_x}) to (pos_y={destination_y}, "
                  f"pos_x={destination_x}) and takes {destination_occupant.get_id()}")

            # DEBUG King needs to have its move validated before it can be considered a possible move
            if isinstance(destination_occupant, King):
                chess_board.render()
                print("ERROR: King is being taken")
