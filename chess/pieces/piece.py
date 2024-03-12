# Piece class
from constants import PieceType, Color

import pygame


class Piece:
    def __init__(
        self,
        board,
        color: Color,
        piece_type: PieceType,
        x_position: int,
        y_position: int,
    ):
        self.moves = []
        self.board = board
        self.color = color
        self.piece_type = piece_type
        self.x_position = x_position
        self.y_position = y_position

    def draw(self, screen, square_size: int, y: int, x: int, piece_letter: str):
        font = pygame.font.Font(None, 40)
        if self.color == Color.WHITE:
            text = font.render(piece_letter, 1, (255, 255, 255))
        else:
            text = font.render(piece_letter, 1, (0, 0, 0))
        text_rect = text.get_rect(center=(x * square_size + square_size / 2, y * square_size + square_size / 2))
        screen.blit(text, text_rect)

    def _calulate_horizontals(self, x_increment, y_increment):
        for i in range(1, 8):
            x = self.x_position + i * x_increment
            y = self.y_position + i * y_increment
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            piece_at_position = self.board.get_piece_at_position(x, y)
            if piece_at_position == None:
                self.moves.append((x, y))
            elif piece_at_position.color != self.color:
                self.moves.append((x, y))
                break
            else:
                break

    def _calculate_diagonals(self, x_direction: int, y_direction: int):
        for i in range(1, 8):
            x = self.x_position + i * x_direction
            y = self.y_position + i * y_direction
            if x < 0 or x > 7 or y < 0 or y > 7:
                break
            piece_at_position = self.board.get_piece_at_position(x, y)
            if piece_at_position == None:
                self.moves.append((x, y))
            elif piece_at_position.color != self.color:
                self.moves.append((x, y))
                break
            else:
                break
