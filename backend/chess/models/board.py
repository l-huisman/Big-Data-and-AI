import numpy as np

import chess.pieces as Pieces


class AoWBoard:
    def __init__(self):
        """
        Initialize the Art of War board
        """
        self.board: np.ndarray = self.init_board()
        self.pieces: list[dict] = self.init_pieces()
        self.pieces_names: tuple = self.get_pieces_names()
        self.resources: list[int] = self.init_resources()

    def reset(self):
        """
        Reset the Art of War board
        """
        self.board = self.init_board()
        self.pieces = self.init_pieces()
        self.pieces_names = self.get_pieces_names()
        self.resources = self.init_resources()

    def get_resources(self, turn: int) -> int:
        """
        Get the resources of the Art of War board
        :param turn: int: The player (Can be 0 or 1)
        :return: int: The resources of the player
        """
        return self.resources[turn]

    def set_resources(self, turn: int, resources: int) -> None:
        """
        Set the resources of the Art of War board
        :param turn: int: The player (Can be 0 or 1)
        :param resources: int: The resources to set
        """
        self.resources[turn] = resources

    def add_resources(self, turn: int, resources: int) -> None:
        """
        Add resources to the Art of War board
        :param turn: int: The player (Can be 0 or 1)
        :param resources: int: The resources to add
        """
        self.resources[turn] += resources

    def remove_resources(self, turn: int, resources: int) -> None:
        """
        Remove resources from the Art of War board
        :param turn: int: The player (Can be 0 or 1)
        :param resources: int: The resources to remove
        """
        self.resources[turn] -= resources

    def get_pieces(self, turn: int) -> dict:
        """
        Get the pieces of the Art of War board
        :param turn: int: The player (Can be 0 or 1)
        :return: dict: The pieces of the player
        """
        return self.pieces[turn]

    def is_piece(self, turn: int, x: int, y: int, piece: Pieces = None) -> bool:
        """
        Check if the piece is in the Art of War board
        :param turn: int: The player (Can be 0 or 1)
        :param x: int: The x coordinate
        :param y: int: The y coordinate
        :param piece: Pieces: The piece to check, if None check for any piece
        :return: bool: If the piece is in the cell
        """
        if piece is None:
            return self.board[turn, x, y] != 0
        return self.board[turn, x, y] == piece

    def get_piece(self, x: int, y: int, turn: int = None) -> Pieces:
        """
        Get the piece of the Art of War board
        :param x: int: The x coordinate
        :param y: int: The y coordinate
        :param turn: int: The player (Can be 0 or 1). If None gets the piece that is not 0 if any
        :return: Pieces: The piece in the cell
        """
        if turn is None:
            for i in range(2):
                if self.board[i, x, y] != 0:
                    return self.board[i, x, y]
            return Pieces.EMPTY
        return self.board[turn, x, y]

    def set_piece(self, turn: int, x: int, y: int, piece: Pieces) -> None:
        """
        Set the piece of the Art of War board
        :param turn: int: The player (Can be 0 or 1)
        :param x: int: The x coordinate
        :param y: int: The y coordinate
        :param piece: Pieces: The piece to set
        """
        self.board[turn, x, y] = piece

    def get_board(self) -> np.ndarray:
        """
        Get the Art of War board
        :return: np.ndarray: The Art of War board
        """
        return self.board

    @staticmethod
    def init_resources() -> list[int]:
        """
        Initialize the resources of the Art of War board
        :return: list[int]: The resources of the players
        """
        return [0, 0]

    @staticmethod
    def init_board() -> np.ndarray:
        """
        Initialize the Art of War board
        :return: np.ndarray: The Art of War board
        """
        board = np.zeros((2, 8, 8), dtype=np.uint8)
        board[:, 0, 3] = Pieces.QUEEN
        board[:, 0, 4] = Pieces.KING
        board[:, 1, :] = Pieces.PAWN
        board[:, 0, (0, 7)] = Pieces.ROOK
        board[:, 0, (1, 6)] = Pieces.KNIGHT
        board[:, 0, (2, 5)] = Pieces.BISHOP
        return board

    @staticmethod
    def init_pieces() -> list[dict]:
        """
        Initialize the Art of War pieces with name and position
        :return: list[dict]: The pieces of the Art of War board
        """
        pieces = {"pawn_1": (1, 0), "pawn_2": (1, 1), "pawn_3": (1, 2), "pawn_4": (1, 3), "pawn_5": (1, 4),
                  "pawn_6": (1, 5), "pawn_7": (1, 6), "pawn_8": (1, 7), "rook_1": (0, 0), "rook_2": (0, 7),
                  "knight_1": (0, 1), "knight_2": (0, 6), "bishop_1": (0, 2), "bishop_2": (0, 5), "queen_1": (0, 3),
                  "king_1": (0, 4), }

        return [pieces.copy(), pieces.copy()]

    def get_state(self, turn: int) -> np.ndarray:
        """
        Get the state of the Art of War board
        :param turn: int: The player (Can be 0 or 1)
        :return: np.ndarray: The state of the player
        """
        arr = self.board.copy()
        if turn == Pieces.WHITE:
            arr[[0, 1]] = arr[[1, 0]]
        return arr.flatten()

    def get_pieces_names(self) -> tuple:
        """
        Get the names of the pieces in the Art of War board
        :return: tuple: The names of the pieces
        """
        zero = list(self.pieces[0].keys())
        one = list(self.pieces[1].keys())
        return zero, one

    def refresh_pieces_names(self) -> None:
        """
        Refresh the names of the pieces in the Art of War board
        """
        self.pieces_names = self.get_pieces_names()

    def set_board(self, board: np.array) -> None:
        """
        Set the Art of War board, pieces and pieces names
        :param board: np.array: The Art of War board
        """
        # TODO: Fix this, when entering a board not wih all complete pieces,
        #  the action mask will be different resulting in a confused AI
        self.board = board
        self.pieces = self.get_pieces_from_board(board)
        self.pieces_names = self.get_pieces_names()

    def get_pieces_from_board(self, board: np.array) -> list[dict]:
        """
        Get the pieces from the Art of War board
        :param board: np.array: The Art of War board
        :return: list[dict]: The pieces of the Art of War board
        """
        pieces_0 = self.get_pieces_from_board_side(board[0])
        pieces_1 = self.get_pieces_from_board_side(board[1])
        return [pieces_0, pieces_1]

    @staticmethod
    def get_pieces_from_board_side(board_side: np.array) -> dict:
        """
        Get the pieces from one side of the Art of War board
        :param board_side: np.array: The side of the Art of War board
        :return: dict: The pieces of the side
        """
        pieces = {}
        counter = 1
        for i, row in enumerate(board_side):
            for j, piece in enumerate(row):
                if piece != 0:
                    name = Pieces.get_piece_name(piece)

                    pieces[name + "_" + str(counter)] = (i, j)
                    counter += 1
        return pieces

    def copy_board(self) -> np.ndarray:
        """
        Copy the Art of War board
        :return: AoWBoard: The copy of the Art of War board
        """
        return np.copy(self.board)
