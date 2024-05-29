import numpy as np

import chess.constants.colors as Colors
from chess.models.types import Cell


class Piece:
    def __init__(self, position: Cell, possibles_length: int, piece_number: int = -1,
                 can_jump: bool = False):
        """
        Initialize the Piece class
        :param color: Colors: The color of the piece
        :param position: Cell: The position of the piece
        :param possibles_length: int: The length of the possible moves array
        :param can_jump: bool: If the piece can jump over other pieces
        """
        self.position: Cell = position
        self.possibles_length: int = possibles_length
        self.can_jump: bool = can_jump
        self.piece_number = piece_number

    def get_piece_number(self) -> int:
        """
        Get the number connected to the piece
        :return:
        """
        return self.piece_number

    def get_position(self) -> Cell:
        """
        Get the position of the piece
        :return: Cell: The position of the piece
        """
        return self.position

    def set_position(self, position: str) -> None:
        """
        Set the position of the piece
        :param position: str: The position of the piece
        """
        self.position = position

    def get_possibles_size(self) -> int:
        """
        Get the size of the possibles array
        :return: int: The size of the possibles array
        """
        return self.possibles_length

    def can_jump(self) -> bool:
        """
        Get if the piece can jump over other pieces
        :return: bool: If the piece can jump over other pieces
        """
        return self.can_jump

    def get_possibles(self) -> np.ndarray:
        """
        Get the possible moves of the piece
        :return: np.ndarray: The possible moves of the piece
        """
        return np.zeros((self.get_possibles_size(), 2), dtype=np.int32)

    def get_empty_actions(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Get the empty actions of the piece
        :return: list: The empty actions of the piece
        """
        possibles = self.get_possibles()
        actions_mask = np.zeros(self.get_possibles_size(), dtype=np.int32)
        return possibles, actions_mask

    def __str__(self) -> str:
        """
        Get the string representation of the piece
        :return: str: The string representation of the piece
        """
        return f"{self.piece_number}"
