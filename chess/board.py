# Board class

import numpy as np
from constants import Color, PieceType
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King

import pygame


class Board:

    def __init__(self):
        self.board = [["" for _ in range(8)] for _ in range(8)]
        self.__initialize_board()

    def __initialize_board(self):
        for i in range(8):
            self.board[i][1] = Pawn(self, Color.WHITE, i, 1)
            self.board[i][6] = Pawn(self, Color.BLACK, i, 6)

        # Rooks
        self.board[0][0] = Rook(self, Color.WHITE, 0, 0)
        self.board[7][0] = Rook(self, Color.WHITE, 7, 0)
        self.board[0][7] = Rook(self, Color.BLACK, 0, 7)
        self.board[7][7] = Rook(self, Color.BLACK, 7, 7)

        # Knights
        self.board[1][0] = Knight(self, Color.WHITE, 1, 0)
        self.board[6][0] = Knight(self, Color.WHITE, 6, 0)
        self.board[1][7] = Knight(self, Color.BLACK, 1, 7)
        self.board[6][7] = Knight(self, Color.BLACK, 6, 7)

        # Bishops
        self.board[2][0] = Bishop(self, Color.WHITE, 2, 0)
        self.board[5][0] = Bishop(self, Color.WHITE, 5, 0)
        self.board[2][7] = Bishop(self, Color.BLACK, 2, 7)
        self.board[5][7] = Bishop(self, Color.BLACK, 5, 7)

        # Queens
        self.board[3][0] = Queen(self, Color.WHITE, 3, 0)
        self.board[3][7] = Queen(self, Color.BLACK, 3, 7)

        # Kings
        self.board[4][0] = King(self, Color.WHITE, 4, 0)
        self.board[4][7] = King(self, Color.BLACK, 4, 7)

    def get_piece_at_position(self, x_position: int, y_position: int) -> Piece:
        return self.board[x_position][y_position]

    def move_piece(self, original_x_position: int, original_y_position: int, new_x_position: int, new_y_position: int):
        piece = self.get_piece_at_position(original_x_position, original_y_position)
        self.board[original_x_position][original_y_position] = ""
        self.board[new_x_position][new_y_position] = piece
        piece.x_position = new_x_position
        piece.y_position = new_y_position

    def draw(self, screen):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = (255, 207, 158)
                else:
                    color = (210, 139, 69)
                pygame.draw.rect(screen, color, (i * 80, j * 80, 80, 80))
                piece: Piece = self.board[i][j]
                if piece != "":
                    piece.draw(screen, 80, j, i)