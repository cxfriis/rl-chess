import numpy as np

from rl_chess.domain.board.ChessBoard import ChessBoard
from rl_chess.domain.board.Tile import Tile
from rl_chess.domain.pieces.Bishop import Bishop
from rl_chess.domain.pieces.King import King
from rl_chess.domain.pieces.Knight import Knight
from rl_chess.domain.pieces.Queen import Queen
from rl_chess.domain.pieces.Rook import Rook
from rl_chess.enums.Enums import Color
from rl_chess.service.PieceMovementService import PieceMovementService


def build_action_grid():
    action_grid = []
    for y_start in range(8):
        for x_start in range(8):
            for y_end in range(8):
                for x_end in range(8):
                    if y_start != y_end or x_start != x_end:
                        action_grid.append((y_start, x_start, y_end, x_end))
    return action_grid


class AgentService:

    ACTION_GRID = build_action_grid()

    piece_movement_service = PieceMovementService()
    color_turn = Color.WHITE

    """
    Action Space
    The agent has a discrete number of actions, such as:
    - select and move piece
    
    I guess all the information the agent should need is the board and its contents... it can figure out what is and 
    isn't allowed as it plays.
    """

    def is_action_legal(self, chess_board: ChessBoard, state, action):
        possible_moves = self.piece_movement_service.get_possible_moves_for_all_pieces_that_can_move(self.color_turn, chess_board)
        action_tuple = self.ACTION_GRID[action]
        y_start = action_tuple[0]
        x_start = action_tuple[1]
        y_end = action_tuple[2]
        x_end = action_tuple[3]

        if chess_board.is_tile_occupied(y_start, x_start):
            piece = chess_board.get_occupant_from_tile(y_start, x_start)
            if piece.get_id() in possible_moves:
                piece_possible_moves = possible_moves.get(piece.get_id())
                if (y_end, x_end) in piece_possible_moves:
                    return True
                    # self.piece_movement_service.move_piece(piece, chess_board, y_end, x_end)
        return False

    def step(self, chess_board: ChessBoard, action):
        """
        Figure out what move the action value represents.
        Determine if move is legal (strongly penalize if not).
        Small penalization if the game is not over.
        Reward if move wins the game.
        :param action:
        :return:
        """
        reward = -0.01
        done = False

        action_tuple = self.ACTION_GRID[action]
        y_start = action_tuple[0]
        x_start = action_tuple[1]
        y_end = action_tuple[2]
        x_end = action_tuple[3]

        color_turn_value = (0 if self.color_turn is Color.BLACK else 1)
        self.piece_movement_service.move_piece(chess_board.get_occupant_from_tile(y_start, x_start), chess_board, y_end, x_end)
        self.color_turn = (Color.WHITE if self.color_turn is Color.BLACK else Color.BLACK)

        # big reward if game is won
        if len(self.piece_movement_service.get_possible_moves_for_all_pieces_that_can_move(self.color_turn, chess_board)) < 1:
            reward = 1
            done = True

        next_state = self.get_state(chess_board)

        return next_state, reward, done

    def get_state(self, chess_board: ChessBoard):
        """
        Return a 1-by-state_size numpy array show the state of the grid.
        Every tile has its own state, encoded as:
        - occupant piece type (where 0 is empty)
        - color of occupant (where 0 is empty, 1 is white, 2 is black)
        """
        # grid_of_floats = [[10 * tile.occupant + tile.occupant.color for tile in row] for row in chess_board.grid]
        grid_of_floats = [[self.get_tile_state(tile) for tile in row] for row in chess_board.grid]
        grid_size = 64
        return np.append(np.reshape(np.array(grid_of_floats), [1, grid_size]), [[(0 if self.color_turn is Color.BLACK else 1)]], axis=1)

    def get_tile_state(self, tile: Tile):
        if tile.is_occupied():
            if isinstance(tile.occupant, King):
                occupant_value = 1
            elif isinstance(tile.occupant, Queen):
                occupant_value = 2
            elif isinstance(tile.occupant, Bishop):
                occupant_value = 3
            elif isinstance(tile.occupant, Knight):
                occupant_value = 4
            elif isinstance(tile.occupant, Rook):
                occupant_value = 5
            else:  # pawn
                occupant_value = 6
        else:
            return 0

        return 10 * occupant_value + (0 if tile.occupant.color is Color.BLACK else 1)
