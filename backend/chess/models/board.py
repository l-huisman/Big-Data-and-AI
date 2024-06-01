import numpy as np

from chess.models.pieces import *
from chess.models import Cell
import chess.pieces as Pieces
from chess.utils.cell import CellUtils


class AoWBoard:
    def __init__(self, length: int = 8, width: int = 8):
        """
        Initialize the Art of War board
        """
        self.board: np.ndarray = self.init_board()
        self.pieces: list[dict] = self.init_pieces()
        self.resources: list[int] = self.init_resources()
        self.length: int = length
        self.width: int = width

    def reset(self):
        """
        Reset the Art of War board
        """
        self.board = self.init_board()
        self.pieces = self.init_pieces()
        self.resources = self.init_resources()

    def is_in_range(self, pos: Cell) -> bool:
        """
        Check if the position is in range of the Art of War board
        @param pos: Cell: The position to check
        @return: bool: If the position is in range
        """
        return 0 <= pos.row < self.length and 0 <= pos.col < self.width

    def get_resources(self, turn: int) -> int:
        """
        Get the resources of the Art of War board
        @param turn: int: The player (Can be 0 or 1)
        @return: int: The resources of the player
        """
        return self.resources[turn]

    def set_resources(self, turn: int, resources: int) -> None:
        """
        Set the resources of the Art of War board
        @param turn: int: The player (Can be 0 or 1)
        @param resources: int: The resources to set
        """
        self.resources[turn] = resources

    def add_resources(self, turn: int, resources: int) -> None:
        """
        Add resources to the Art of War board
        @param turn: int: The player (Can be 0 or 1)
        @param resources: int: The resources to add
        """
        self.resources[turn] += resources

    def remove_resources(self, turn: int, resources: int) -> None:
        """
        Remove resources from the Art of War board
        @param turn: int: The player (Can be 0 or 1)
        @param resources: int: The resources to remove
        """
        self.resources[turn] -= resources

    def get_pieces(self, turn: int) -> dict:
        """
        Get the pieces of the Art of War board
        @param turn: int: The player (Can be 0 or 1)
        @return: dict: The pieces of the player
        """
        return self.pieces[turn]

    def is_piece(self, turn: int, pos: Cell, piece: Piece = None) -> bool:
        """
        Check if the piece is in the Art of War board
        @param turn: int: The player (Can be 0 or 1)
        @param pos: Cell: The position to check the piece (row, col)
        @param piece: Pieces: The piece to check, if None check for any piece
        @return: bool: If the piece is in the cell
        """
        if pos.__class__ is not Cell:
            pos = Cell(pos[0], pos[1])
        if piece is None:
            return not isinstance(self.board[turn, pos.row, pos.col], Empty)
        return isinstance(self.board[turn, pos.row, pos.col], piece.__class__)

    def get_piece(self, pos: Cell, turn: int = None) -> Piece:
        """
        Get the piece of the Art of War board
        @param pos: Cell: The position to get the piece (row, col)
        @param turn: int: The player (Can be 0 or 1). If None gets the piece that is not 0 if any
        @return: Pieces: The piece in the cell
        """
        pos = CellUtils.make_cell(pos)

        if turn is None:
            for i in range(2):
                if not isinstance(self.board[i, pos.row, pos.col], Empty):
                    return self.board[i, pos.row, pos.col]
            return Empty()
        return self.board[turn, pos.row, pos.col]

    def set_piece(self, turn: int, pos: Cell, piece: Piece) -> None:
        """
        Set the piece of the Art of War board
        @param turn: int: The player (Can be 0 or 1)
        @param pos: Cell: The position to set the piece (row, col)
        @param piece: Pieces: The piece to set
        """
        pos = CellUtils.make_cell(pos)
        self.board[turn, pos.row, pos.col] = piece

    def get_board(self) -> np.ndarray:
        """
        Get the Art of War board
        @return: np.ndarray: The Art of War board
        """
        return self.board

    @staticmethod
    def init_resources() -> list[int]:
        """
        Initialize the resources of the Art of War board
        @return: list[int]: The resources of the players
        """
        return [0, 0]

    @staticmethod
    def init_board() -> np.ndarray:
        """
        Initialize the Art of War board
        @return: np.ndarray: The Art of War board
        """
        board = np.zeros((2, 8, 8), dtype=Piece)
        board[:, :, :] = Empty()
        board[:, 0, 3] = Queen()
        board[:, 0, 4] = King()
        board[:, 1, :] = Pawn()
        board[:, 0, (0, 7)] = Rook()
        board[:, 0, (1, 6)] = Knight()
        board[:, 0, (2, 5)] = Bishop()
        return board

    @staticmethod
    def init_pieces() -> list[dict]:
        """
        Initialize the Art of War pieces with name and position
        @return: list[dict]: The pieces of the Art of War board
        """
        pieces = {"pawn_1": (1, 0), "pawn_2": (1, 1), "pawn_3": (1, 2), "pawn_4": (1, 3), "pawn_5": (1, 4),
                  "pawn_6": (1, 5), "pawn_7": (1, 6), "pawn_8": (1, 7), "rook_1": (0, 0), "rook_2": (0, 7),
                  "knight_1": (0, 1), "knight_2": (0, 6), "bishop_1": (0, 2), "bishop_2": (0, 5), "queen_1": (0, 3),
                  "king_1": (0, 4), }

        return [pieces.copy(), pieces.copy()]

    def get_state(self, turn: int) -> np.ndarray:
        """
        Get the state of the Art of War board
        @param turn: int: The player (Can be 0 or 1)
        @return: np.ndarray: The state of the player
        """
        arr = self.get_numeric_board()
        if turn == Pieces.WHITE:
            arr[[0, 1]] = arr[[1, 0]]
        return arr.flatten()

    def get_numeric_board(self) -> np.ndarray:
        """
        Get the numeric board of the Art of War board
        @return: np.ndarray: The numeric board of the Art of War board
        """
        numeric_board = np.zeros((2, 8, 8), dtype=int)
        for i in range(2):
            for j in range(8):
                for k in range(8):
                    numeric_board[i, j, k] = self.board[i, j, k].__str__()
        return numeric_board

    def get_pieces_names(self) -> tuple:
        """
        Get the names of the pieces in the Art of War board
        @return: tuple: The names of the pieces for both sides
        """
        zero = list(self.pieces[0].keys())
        one = list(self.pieces[1].keys())
        return zero, one

    def set_board(self, board: np.array) -> None:
        """
        Set the Art of War board, pieces and pieces names
        @param board: np.array: The Art of War board
        """
        # TODO: Fix this, when entering a board not with all pieces,
        #  the action mask will be different resulting in a confused AI
        for i in range(2):
            for j in range(8):
                for k in range(8):
                    self.board[i, j, k] = self.get_piece_from_number(board[i, j, k])
        self.pieces = self.get_pieces_from_board(board)
        self.pieces_names = self.get_pieces_names()

    def get_piece_from_number(self, number: int) -> Piece:
        """
        Get the piece from the Art of War board
        @param number: int: The number of the piece
        @return: Pieces: The piece of the Art of War board
        """
        return { # TODO: Fix this
            0: Empty(),
            1: Pawn(),
            2: Bishop(),
            3: Knight(),
            4: Rook(),
            5: Queen(),
            6: King(),
            7: Wingedknight(),
            8: Hoplite(),
            9: Warelephant(),
        }[number]

    def get_pieces_from_board(self, board: np.array) -> list[dict]:
        """
        Get the pieces from the Art of War board
        @param board: np.array: The Art of War board
        @return: list[dict]: The pieces of the Art of War board
        """
        pieces_0 = self.get_pieces_from_board_side(board[0])
        pieces_1 = self.get_pieces_from_board_side(board[1])
        return [pieces_0, pieces_1]

    def get_pieces_from_board_side(self, board_side: np.array) -> dict:
        """
        Get the pieces from one side of the Art of War board
        @param board_side: np.array: The side of the Art of War board
        @return: dict: The pieces of the side
        """
        pieces = {}
        counter = 1
        for i, row in enumerate(board_side):
            for j, piece in enumerate(row):
                if piece != 0:
                    name = self.get_piece_from_number(piece).__class__.__name__.lower()

                    pieces[name + "_" + str(counter)] = (i, j)
                    counter += 1
        return pieces

    def copy_board(self) -> np.ndarray:
        """
        Copy the Art of War board
        @return: AoWBoard: The copy of the Art of War board
        """
        return np.copy(self.board)

    def get_king_position(self, turn: int) -> Cell:
        """
        Get the position of the king in the Art of War board
        @param turn: int: The player (Can be 0 or 1)
        @return: Cell: The position of the king
        """
        for i in range(8):
            for j in range(8):
                if self.is_piece(turn, Cell(i, j), King()):
                    return Cell(i, j)
        print(self.get_numeric_board())
        assert False, f"King not found for {turn}"

    def is_enemy_piece(self, pos: Cell, turn: int) -> bool:
        """
        Check if the piece is an enemy piece
        @param pos: Cell: The position to check
        @param turn: int: The player (Can be 0 or 1)
        @return: bool: If the piece is an enemy piece
        """
        pos = CellUtils.make_cell(pos)
        return not self.is_empty(Cell(7 - pos.row, pos.col), 1 - turn)

    def is_empty(self, pos: Cell, turn: int) -> bool:
        """
        Check if the cell is empty
        @param pos: Cell: The position to check
        @param turn: int: The player (Can be 0 or 1)
        @return: bool: If the cell is empty
        """
        return self.is_piece(turn, CellUtils.make_cell(pos), Empty())

    def is_empty_or_pawn(self, pos: Cell, turn: int) -> bool:
        """
        Check if the cell is empty or a pawn
        @param pos: Cell: The position to check
        @param turn: int: The player (Can be 0 or 1)
        @return: bool: If the cell is empty or a pawn
        """
        return self.is_empty(pos, turn) or self.is_piece(turn, pos, Pieces.PAWN) or \
            self.is_piece(turn, pos, Pieces.HOPLITE)

    def is_enemy_king(self, pos: Cell, turn: int) -> bool:
        """
        Check if the piece is an enemy king
        @param pos: Cell: The position to check
        @param turn: int: The player (Can be 0 or 1)
        @return: bool: If the piece is an enemy king
        """
        r, c = pos
        return self.is_piece(1 - turn, Cell(7 - r, c), Pieces.KING)

    def is_tile_empty_on_both_side(self, pos: Cell, turn: int) -> bool:
        """
        Check if the tile is empty on both sides of the board
        @param pos: Cell: The position to check
        @param turn: int: The player (Can be 0 or 1)
        @return: bool: If the tile is empty on both sides
        """
        r, c = pos
        return self.is_empty(Cell(r, c), turn) and self.is_empty(Cell(7 - r, c), 1 - turn)

    def is_tile_empty_or_pawn_on_both_side(self, pos: Cell, turn: int) -> bool:
        """
        Check if the tile is empty or a pawn on both sides of the board
        @param pos: Cell: The position to check
        @param turn: int: The player (Can be 0 or 1)
        @return: bool: If the tile is empty or a pawn on both sides
        """
        r, c = pos
        return self.is_empty_or_pawn(pos, turn) and self.is_empty_or_pawn(Cell(7 - r, c), 1 - turn)

    def general_validation(self, current_pos: Cell, next_pos: Cell, turn: int, deny_enemy_king: bool) -> bool:
        """
        General validation for the move
        @param current_pos: Cell: The current position
        @param next_pos: Cell: The next position
        @param turn: int: The player (Can be 0 or 1)
        @param deny_enemy_king: bool: If the enemy king should be denied
        @return bool: If the move is valid
        """
        if not self.is_in_range(next_pos):
            return False

        if not self.is_empty(next_pos, turn):
            return False

        if (self.is_enemy_king(next_pos, turn) or self.is_piece(pos=next_pos, turn=turn, piece=King())) and (not deny_enemy_king):
            return False

        if not self.is_path_empty_for_piece(current_pos, next_pos, turn):
            return False
        return True

    def is_valid_move(
            self,
            current_pos: Cell,
            next_pos: Cell,
            turn: int,
            deny_enemy_king: bool,
    ) -> bool:
        """
        Check if the move is valid
        @param current_pos: Cell: The current position
        @param next_pos: Cell: The next position
        @param turn: int: The player (Can be 0 or 1)
        @param deny_enemy_king: bool: If the enemy king should be denied
        @return: bool: If the move is valid
        """
        if not self.general_validation(current_pos, next_pos, turn, deny_enemy_king):
            return False
        if self.is_lead_to_check(current_pos, next_pos, turn):
            return False
        return True

    def is_lead_to_check(self, current_pos: Cell, next_pos: Cell, turn: int) -> bool:
        """
        Check if the move leads to a check
        @param current_pos: Cell: The current position
        @param next_pos: Cell: The next position
        @param turn: int: The player (Can be 0 or 1)
        @return: bool: If the move leads to a check
        """
        # Added import here, otherwise you will get circular imports
        from chess import Chess
        temp = Chess(render_mode="rgb_array")
        temp.aow_board.board = self.copy_board()
        temp.move_piece(current_pos, next_pos, turn)
        return temp.is_check(temp.aow_board.get_king_position(turn), turn)

    def is_path_empty_for_piece(self, current_pos: Cell, next_pos: Cell, turn: int) -> bool:
        """
        Check if the path is empty for the piece
        @param current_pos: Cell: The current position
        @param next_pos: Cell: The next position
        @param turn: int: The player (Can be 0 or 1)
        @return: bool: If the path is empty for the piece
        """
        # TODO: This could be improved
        piece = self.get_piece(current_pos, turn)
        this_piece = None
        for dic in self.pieces:
            for key, val in dic.items():
                if val == current_pos:
                    this_piece = key.split("_")[0]

        # ! Especially this one
        if this_piece == "warelephant":
            return self.is_path_empty(current_pos, next_pos, turn, except_pawn=True)
        else:
            return piece.can_jump() or (self.is_path_empty(current_pos, next_pos, turn))

    def is_path_empty(self, current_pos: Cell, next_pos: Cell, turn: int, except_pawn: bool = False) -> bool:
        """
        Check if the path between two positions is empty
        @param current_pos: Cell: The current position
        @param next_pos: Cell: The next position
        @param turn: int: The player (Can be 0 or 1)
        @param except_pawn: bool: If the path should ignore pawns
        @return: bool: If the path between the two positions is empty
        """
        path = self.get_path(current_pos, next_pos)

        for pos in path:
            if pos == current_pos:
                continue

            if not self.is_tile_empty_on_both_side(pos, turn):
                if except_pawn and self.is_piece(turn, pos, Pawn()):
                    except_pawn = False
                    continue
                return False
        return True

    @staticmethod
    def get_path(current_pos: Cell, next_pos: Cell) -> list[Cell]:
        """
        Get the path between two positions
        @param current_pos: Cell: The current position
        @param next_pos: Cell: The next position
        @return: list[Cell]: The path between the two positions
        """
        current_pos = CellUtils.make_cell(current_pos)
        next_pos = CellUtils.make_cell(next_pos)

        diff_row = next_pos.row - current_pos.row
        diff_col = next_pos.col - current_pos.col
        size = max(abs(diff_row), abs(diff_col)) - 1

        # Get direction +1 for positive difference, 0 for no difference and -1 for negative difference
        sign_row = np.sign(next_pos.row - current_pos.row)
        sign_col = np.sign(next_pos.col - current_pos.col)

        # Initializing Path array
        rows = np.zeros(size, dtype=np.int32) + next_pos.row
        cols = np.zeros(size, dtype=np.int32) + next_pos.col

        # Filling Path array
        if diff_row:
            rows = np.arange(current_pos.row + sign_row, next_pos.row, sign_row, dtype=np.int32)

        if diff_col:
            cols = np.arange(current_pos.col + sign_col, next_pos.col, sign_col, dtype=np.int32)

        return [Cell(row, col) for row, col in zip(rows, cols)]

