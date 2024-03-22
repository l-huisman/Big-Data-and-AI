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
        if x_position < 0 or x_position > 7 or y_position < 0 or y_position > 7:
            return None
        return self.board[x_position][y_position]


    def move_piece(self, original_position: tuple, new_position: tuple) -> None:
        x_original, y_original = original_position
        x_new, y_new = new_position
        
        # Check if the piece is a King and the move is a castling move
        if isinstance(self.board[x_original][y_original], King) and abs(x_original - x_new) == 2:
            # Check if it's a kingside castling
            if x_new > x_original:
                # Move the rook to the left of the king
                self.board[x_new - 1][y_new] = self.board[7][y_new]
                self.board[7][y_new] = None
                # Update the rook's position
                self.board[x_new - 1][y_new].x_position = x_new - 1
                self.board[x_new - 1][y_new].y_position = y_new
            # Check if it's a queenside castling
            else:
                # Move the rook to the right of the king
                self.board[x_new + 1][y_new] = self.board[0][y_new]
                self.board[0][y_new] = None
                # Update the rook's position
                self.board[x_new + 1][y_new].x_position = x_new + 1
                self.board[x_new + 1][y_new].y_position = y_new

        # Move the piece
        self.board[x_new][y_new] = self.board[x_original][y_original]
        self.board[x_original][y_original] = None

        # Check for pawn promotion
        if isinstance(self.board[x_new][y_new], Pawn):
            if (self.board[x_new][y_new].color is Color.WHITE and y_new == 0) or (
                self.board[x_new][y_new].color is Color.BLACK and y_new == 7
            ):
                self.promote_pawn(x_new, y_new)

        self.is_white_turn = not self.is_white_turn
        if self.is_white_turn:
            self.round += 1

    def promote_pawn(self, x: int, y: int) -> None:
        # Ask the player which piece to promote to
        promotion_options = ["Queen", "Rook", "Bishop", "Knight"]
        chosen_piece = None
        while chosen_piece not in promotion_options:
            print("Choose a piece to promote your pawn:")
            print("1. Queen")
            print("2. Rook")
            print("3. Bishop")
            print("4. Knight")
            choice = input("Enter the number of your choice: ")
            if choice == "1":
                chosen_piece = "Queen"
            elif choice == "2":
                chosen_piece = "Rook"
            elif choice == "3":
                chosen_piece = "Bishop"
            elif choice == "4":
                chosen_piece = "Knight"
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

        # Replace the pawn with the chosen piece
        if chosen_piece == "Queen":
            self.board[x][y] = Queen(self, self.board[x][y].color, x, y)
        elif chosen_piece == "Rook":
            self.board[x][y] = Rook(self, self.board[x][y].color, x, y)
        elif chosen_piece == "Bishop":
            self.board[x][y] = Bishop(self, self.board[x][y].color, x, y)
        elif chosen_piece == "Knight":
            self.board[x][y] = Knight(self, self.board[x][y].color, x, y)

        # Update selected piece to the newly promoted piece
        self.__selected_piece = self.board[x][y]

    def draw(self, screen):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = (255, 207, 158)
                else:
                    color = (210, 139, 69)
                pygame.draw.rect(screen, color, (i * 80, j * 80, 80, 80))
                piece: Piece = self.board[i][j]
                if piece is not None:
                    piece.draw(screen, 80, j, i)

                    # Check if the piece is selected and update selected piece
                    if self.__selected_piece is not None and self.__selected_piece == piece:
                        self.__selected_piece = piece

        # Draw possible moves for selected piece only if it's the player's turn
        if self.__selected_piece is not None and self.is_white_turn == (self.__selected_piece.color is Color.WHITE):
            self.draw_possible_moves(screen, self.__selected_piece)

        # Draw round
        font = pygame.font.Font(None, 36)
        text = font.render(f"Round: {self.round}", True, (255, 0, 0))
        screen.blit(text, (10, 10))

        # Draw whose turn it is
        turn = "White" if self.is_white_turn else "Black"
        text = font.render(f"Turn: {turn}", True, (255, 0, 0))
        screen.blit(text, (10, 50))


    def draw_possible_moves(self, screen, clicked_piece: Piece):
        if clicked_piece is None:
            return

        possible_moves = clicked_piece.get_possible_moves()
        if possible_moves is None:
            return

        for move in possible_moves:
            center = (move[0] * 80 + 40, move[1] * 80 + 40)
            pygame.draw.circle(screen, (37, 12, 127), center, 10, 0)

    def get_selected_piece(self):
        return self.__selected_piece

    def set_selected_piece(self, piece: Piece):
        self.__selected_piece = piece
