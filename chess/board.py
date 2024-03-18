from constants import Color
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King

import pygame


class Board:

    def __init__(self) -> None:
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.__selected_piece = None
        self.__initialize_board()
        self.round = 0
        self.is_white_turn = True

    def __initialize_board(self) -> None:
        self.round = 1
        self.is_white_turn = True
        for i in range(8):
            self.board[i][1] = Pawn(self, Color.BLACK, i, 1)
            self.board[i][6] = Pawn(self, Color.WHITE, i, 6)

        # Rooks
        self.board[0][0] = Rook(self, Color.BLACK, 0, 0)
        self.board[7][0] = Rook(self, Color.BLACK, 7, 0)
        self.board[0][7] = Rook(self, Color.WHITE, 0, 7)
        self.board[7][7] = Rook(self, Color.WHITE, 7, 7)

        # Knights
        self.board[1][0] = Knight(self, Color.BLACK, 1, 0)
        self.board[6][0] = Knight(self, Color.BLACK, 6, 0)
        self.board[1][7] = Knight(self, Color.WHITE, 1, 7)
        self.board[6][7] = Knight(self, Color.WHITE, 6, 7)

        # Bishops
        self.board[2][0] = Bishop(self, Color.BLACK, 2, 0)
        self.board[5][0] = Bishop(self, Color.BLACK, 5, 0)
        self.board[2][7] = Bishop(self, Color.WHITE, 2, 7)
        self.board[5][7] = Bishop(self, Color.WHITE, 5, 7)

        # Queens
        self.board[3][0] = Queen(self, Color.BLACK, 3, 0)
        self.board[3][7] = Queen(self, Color.WHITE, 3, 7)

        # Kings
        self.board[4][0] = King(self, Color.BLACK, 4, 0)
        self.board[4][7] = King(self, Color.WHITE, 4, 7)

    def get_piece_at_position(self, x_position: int, y_position: int) -> Piece | None:
        return self.board[x_position][y_position]

    def move_piece(self, original_position: tuple, new_position: tuple) -> None:
        x_original, y_original = original_position
        x_new, y_new = new_position
        
        # Check if the piece exists and matches the current turn
        piece = self.board[x_original][y_original]
        if piece is None or (piece.color is Color.WHITE and not self.is_white_turn) \
            or (piece.color is Color.BLACK and self.is_white_turn):
            return  # Invalid move, not the turn of this color
        
        # Move the piece
        self.board[x_new][y_new] = self.board[x_original][y_original]
        self.board[x_original][y_original] = None
        self.is_white_turn = not self.is_white_turn
        if self.is_white_turn:
            self.round += 1

    def draw(self, screen):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = (255, 207, 158)
                else:
                    color = (210, 139, 69)
                pygame.draw.rect(screen, color, (i * 80, j * 80, 80, 80))
                piece: Piece = self.board[i][j]
                if piece != None:
                    piece.draw(screen, 80, j, i)

                if self.__selected_piece != None:
                    self.draw_possible_moves(screen, self.__selected_piece)
        # Draw round
        font = pygame.font.Font(None, 36)
        text = font.render(f"Round: {self.round}", True, (255, 0, 0))
        screen.blit(text, (10, 10))

        # Draw whose turn it is
        turn = "White" if self.is_white_turn else "Black"
        text = font.render(f"Turn: {turn}", True, (255, 0, 0))
        screen.blit(text, (10, 50))

    def draw_possible_moves(self, screen, clicked_piece: Piece) -> None:
        if clicked_piece.color is Color.WHITE and self.is_white_turn is False:
            return
        if clicked_piece.color is Color.BLACK and self.is_white_turn is True:
            return
        possible_moves = clicked_piece.get_possible_moves()
        for move in possible_moves:
            center = (move[0] * 80 + 40, move[1] * 80 + 40)
            pygame.draw.circle(screen, (37, 12, 127), center, 10, 0)

    def get_selected_piece(self) -> Piece | None:
        return self.__selected_piece

    def set_selected_piece(self, piece: Piece) -> None:
        self.__selected_piece = piece
