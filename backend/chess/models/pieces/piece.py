import numpy as np

from chess.models.types import Cell


class Piece:
    def __init__(self, possibles_length: int, position: Cell | None = None, piece_number: int = -1,
                 can_jump: bool = False, upgradable: bool = False, upgrade_options: list['Piece'] = None):
        """
        Initialize the Piece class
        @param color: Colors: The color of the piece
        @param position: Cell: The position of the piece
        @param possibles_length: int: The length of the possible moves array
        @param can_jump: bool: If the piece can jump over other pieces
        """
        if upgrade_options is None:
            upgrade_options = []

        self.position: Cell = position
        self.possibles_length: int = possibles_length
        self.jump: bool = can_jump
        self.piece_number = piece_number
        self.is_on_board = True
        self.upgradable = upgradable
        self.upgrade_options = upgrade_options
        self.moved = False

    def get_piece_number(self) -> int:
        """
        Get the number connected to the piece
        @return:
        """
        return self.piece_number

    def has_moved(self) -> bool:
        """
        Get if the piece has moved
        @return: bool: If the piece has moved
        """
        return self.moved

    def is_on_board(self) -> bool:
        """
        Get if the piece is on the board
        @return: bool: If the piece is on the board
        """
        return self.is_on_board

    def set_is_on_board(self, is_on_board: bool) -> None:
        """
        Set if the piece is on the board
        @param is_on_board: bool: If the piece is on the board
        """
        self.is_on_board = is_on_board

    def set_has_moved(self, has_moved: bool = True) -> None:
        """
        Set if the piece has moved
        @param has_moved: bool: If the piece has moved
        """
        self.moved = has_moved

    def get_upgrade_options(self) -> list['Piece']:
        """
        Get the upgrade options of the piece
        @return: list: The upgrade options of the piece
        """
        return self.upgrade_options

    def get_position(self) -> Cell:
        """
        Get the position of the piece
        @return: Cell: The position of the piece
        """
        return self.position

    def set_position(self, position: str) -> None:
        """
        Set the position of the piece
        @param position: str: The position of the piece
        """
        self.position = position

    def get_possibles_size(self) -> int:
        """
        Get the size of the possibles array
        @return: int: The size of the possibles array
        """
        return self.possibles_length

    def is_upgradable(self) -> bool:
        """
        Get if the piece can be upgraded
        @return: bool: If the piece can be upgraded
        """
        return self.upgradable

    def can_jump(self) -> bool:
        """
        Get if the piece can jump over other pieces
        @return: bool: If the piece can jump over other pieces
        """
        return self.jump

    def get_possibles(self) -> np.ndarray:
        """
        Get the possible moves of the piece
        @return: np.ndarray: The possible moves of the piece
        """
        return np.zeros((self.get_possibles_size(), 2), dtype=np.int32)

    def get_empty_actions(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Get the empty actions of the piece
        @return: list: The empty actions of the piece
        """
        possibles = self.get_possibles()
        actions_mask = np.zeros(self.get_possibles_size(), dtype=np.int32)
        return possibles, actions_mask

    def get_name(self):
        """
        Get the name of the piece
        @return: str: The name of the piece
        """
        return f"{self.__class__.__name__}"

    def get_actions(self, board: 'AoWBoard', pos: Cell | None, turn: int, deny_enemy_king: bool = False) -> tuple:
        """
        Get the actions of the piece
        @param board: np.ndarray: The Art of War board
        @return: tuple: The actions of the piece
        """
        possibles, actions_mask = self.get_empty_actions()

        if pos is None and self.position is None:
            return possibles, actions_mask

        if pos is None:
            pos = self.position

        for i, (r, c) in enumerate(self.get_moves()):

            if board.is_valid_move(pos, Cell(pos[0] + r, pos[1] + c), turn, deny_enemy_king):
                next_pos = Cell(pos[0] + r, pos[1] + c)
                possibles[i] = next_pos
                actions_mask[i] = 1

        return possibles, actions_mask

    def get_moves(self) -> tuple:
        """
        Get the moves of the piece
        @return: list: The moves of the piece
        """
        pass

    def __str__(self) -> str:
        """
        Get the string representation of the piece
        @return: str: The string representation of the piece
        """
        return f"{self.piece_number}"
