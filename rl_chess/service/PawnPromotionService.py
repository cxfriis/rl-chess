from rl_chess.domain.board.ChessBoard import ChessBoard
from rl_chess.domain.pieces.Bishop import Bishop
from rl_chess.domain.pieces.Knight import Knight
from rl_chess.domain.pieces.Pawn import Pawn
from rl_chess.domain.pieces.Piece import Piece
from rl_chess.domain.pieces.Queen import Queen
from rl_chess.domain.pieces.Rook import Rook
from rl_chess.enums.Enums import Color


class PawnPromotionService:

    @staticmethod
    def is_eligible_for_promotion(piece: Piece) -> bool:
        if isinstance(piece, Pawn):
            pos_y = piece.coords[0]
            if (piece.color == Color.WHITE and pos_y == 0) or (piece.color == Color.BLACK and pos_y == 7):
                return True
        else:
            return False

    @staticmethod
    def promote_to_queen(pawn: Pawn, chess_board: ChessBoard) -> None:
        queen = Queen(pawn.coords[0], pawn.coords[1], pawn.color)
        PawnPromotionService.__promote_pawn(pawn, queen, chess_board)

    @staticmethod
    def promote_to_rook(pawn: Pawn, chess_board: ChessBoard) -> None:
        rook = Rook(pawn.coords[0], pawn.coords[1], pawn.color)
        PawnPromotionService.__promote_pawn(pawn, rook, chess_board)

    @staticmethod
    def promote_to_knight(pawn: Pawn, chess_board: ChessBoard) -> None:
        knight = Knight(pawn.coords[0], pawn.coords[1], pawn.color)
        PawnPromotionService.__promote_pawn(pawn, knight, chess_board)

    @staticmethod
    def promote_to_bishop(pawn: Pawn, chess_board: ChessBoard) -> None:
        bishop = Bishop(pawn.coords[0], pawn.coords[1], pawn.color)
        PawnPromotionService.__promote_pawn(pawn, bishop, chess_board)

    @staticmethod
    def __promote_pawn(pawn: Pawn, promoted_piece: Piece, chess_board: ChessBoard) -> None:
        PawnPromotionService.__remove_pawn(pawn, chess_board)
        PawnPromotionService.__name_occupant(promoted_piece, chess_board)
        chess_board.add_occupant(promoted_piece)

    @staticmethod
    def __remove_pawn(piece: Piece, chess_board: ChessBoard) -> None:
        piece.alive = False
        pos_y = piece.coords[0]
        pos_x = piece.coords[1]
        chess_board.remove_occupant_from_tile(pos_y, pos_x)

    @staticmethod
    def __name_occupant(promoted_piece: Piece, chess_board: ChessBoard) -> None:
        pieces = chess_board.white_pieces if promoted_piece.color == Color.WHITE else chess_board.black_pieces

        # this only works if captured items have 'alive' set to False, but aren't actually removed from the map
        if isinstance(promoted_piece, Queen):
            type_count = len(list(filter(lambda item: isinstance(item[1], Queen), pieces.items())))
            promoted_piece.short_name = f"Qu_{type_count}"
        elif isinstance(promoted_piece, Rook):
            type_count = len(list(filter(lambda item: isinstance(item[1], Rook), pieces.items())))
            promoted_piece.short_name = f"Ro_{type_count}"
        elif isinstance(promoted_piece, Knight):
            type_count = len(list(filter(lambda item: isinstance(item[1], Knight), pieces.items())))
            promoted_piece.short_name = f"Kn_{type_count}"
        elif isinstance(promoted_piece, Bishop):
            type_count = len(list(filter(lambda item: isinstance(item[1], Bishop), pieces.items())))
            promoted_piece.short_name = f"Bi_{type_count}"
