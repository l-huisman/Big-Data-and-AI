from typing import Union

import numpy as np
import pygame
from pygame.font import Font
from pygame.surface import Surface

import chess.constants.colors as Colors
import chess.pieces as Pieces
from chess.models import Cell
from chess.models.board import AoWBoard
from chess.models.pieces import Piece


class PyGameUtils:

    def __init__(self, window_size: int, render_mode: str) -> None:
        """
        Initialize the PyGameUtils class
        :param window_size: int: The size of the window
        :param render_mode: str: The render mode
        """
        self.font: Font | None = None
        self.cell_size: int = window_size // 8
        self.screen: Surface | None = None
        self.window_size: int = window_size
        self.render_mode: str = render_mode

    def draw_cells(self) -> None:
        """
        Draw the Art of War board cells
        """
        for y in range(8):
            for x in range(8):
                self.draw_cell(x, y)

    def draw_pieces(self, board: np.ndarray) -> None:
        """
        Draw the Art of War pieces
        :param board: np.ndarray: The Art of War board
        """
        for y in range(8):
            for x in range(8):
                self.draw_piece(x, y, board)

    def draw_axis(self) -> None:
        """
        Draw the axis labels (a-h, 1-8)
        """
        font = pygame.font.Font(None, 36)
        for i, label in enumerate("abcdefgh"):
            text = font.render(label, True, Colors.GREEN)
            self.screen.blit(text, (i * self.cell_size + self.cell_size // 2 - 10, self.window_size - 20))
        for i, label in enumerate("12345678"):
            text = font.render(label, True, Colors.GREEN)
            self.screen.blit(text, (self.window_size - 20, i * self.cell_size + self.cell_size // 2 - 10))

    def render(self, board: np.ndarray) -> Union[None, np.ndarray]:
        """
        Render the Art of War board
        :param board: np.ndarray: The Art of War board
        :return: Union[None, np.ndarray]: The rendered Art of War board
        """
        self.init_pygame()
        self.screen.fill(Colors.BLACK)
        self.draw_cells()
        self.draw_pieces(board)
        self.draw_axis()

        if self.render_mode == "human":
            pygame.display.flip()
        else:
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

    def init_pygame(self) -> None:
        """
        Initialize the PyGame environment for Art of War
        """
        if self.screen is not None:
            return
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("chess/seguisym.ttf", self.cell_size // 2)

        if self.render_mode == "human":
            pygame.display.init()
            self.screen = pygame.display.set_mode((self.window_size,) * 2)
            pygame.display.set_caption("Art of War RL Environment")
        else:
            self.screen = pygame.Surface((self.window_size,) * 2)

    @staticmethod
    def get_cell_color(x: int, y: int) -> tuple[int]:
        """
        Get the color of the cell (for the pattern in the board)
        :param x: int: The x coordinate
        :param y: int: The y coordinate
        :return: tuple[int]: The color of the cell
        """
        if (x + y) % 2 == 0:
            return Colors.GRAY
        return Colors.BLACK

    def get_left_top(self, x: int, y: int, offset: float = 0) -> tuple[float, float]:
        """
        Get the left top coordinates of the cell
        :param x: int: The x coordinate
        :param y: int: The y coordinate
        :param offset: float: The offset
        :return: tuple[float, float]: The left top coordinates of the cell
        """
        return self.cell_size * x + offset, self.cell_size * y + offset

    def draw_cell(self, x: int, y: int) -> None:
        """
        Draw the cell (tile/square)
        :param x: int: The x coordinate
        :param y: int: The y coordinate
        """
        pygame.draw.rect(
            self.screen,
            self.get_cell_color(x, y),
            pygame.Rect((*self.get_left_top(x, y), self.cell_size, self.cell_size)),
        )

    def draw_piece(self, x: int, y: int, board: np.ndarray) -> None:
        """
        Draw the piece on the cell
        :param x: int: The x coordinate
        :param y: int: The y coordinate
        :param board: np.ndarray: The Art of War board
        """
        row, col = y, x
        for color in [Pieces.BLACK, Pieces.WHITE]:

            if board[color, row, col] == Pieces.EMPTY:
                continue

            yy = abs((color * 7) - y)
            text = self.font.render(
                Pieces.get_ascii(color, int(board[color, row, col])),
                True,
                Colors.WHITE,
                self.get_cell_color(x, yy),
            )
            rect = text.get_rect()
            rect.center = self.get_left_top(x, yy, offset=self.cell_size // 2)
            self.screen.blit(text, rect)

    def close(self) -> None:
        """
        Close the PyGame environment
        """
        if self.screen is None:
            return

        pygame.display.quit()
        pygame.quit()
