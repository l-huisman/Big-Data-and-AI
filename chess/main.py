import pygame
from board import Board
from pieces import Piece
from constants import Color

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = (640, 640)
FPS = 12

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a chess board
chess_board = Board()


# Function to get the position of the mouse
def get_mouse_position(mouse_position: tuple) -> tuple:
    mouse_x = mouse_position[0] // 80
    mouse_y = mouse_position[1] // 80
    return mouse_x, mouse_y


# Game loop
running = True
while running:
    # Keep the loop running at the right speed
    pygame.time.Clock().tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing the window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                print("Resetting board")
                chess_board.reset_board()
        # Check for mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            mouse_pos = pygame.mouse.get_pos()
            x, y = get_mouse_position(mouse_pos)

            # Get the selected piece and clicked piece
            selected_piece: Piece = chess_board.get_selected_piece()
            clicked_piece: Piece = chess_board.get_piece_at_position(x, y)

            # Check if it's the turn of the color of the selected piece
            if selected_piece is not None and selected_piece.color is not Color.WHITE and chess_board.is_white_turn:
                continue  # Disallow move for non-white pieces on white's turn
            elif selected_piece is not None and selected_piece.color is not Color.BLACK and not chess_board.is_white_turn:
                continue  # Disallow move for non-black pieces on black's turn

            # Handling logic when a piece is selected
            if selected_piece is not None:
                if (x, y) in selected_piece.get_possible_moves():
                    chess_board.move_piece(selected_piece.get_position(), (x, y))
                    selected_piece.set_position(x, y)
                    selected_piece.set_has_moved()
                chess_board.set_selected_piece(None)
            elif clicked_piece is not None and clicked_piece.color == Color.WHITE and chess_board.is_white_turn:
                chess_board.draw_possible_moves(screen, clicked_piece)
                chess_board.set_selected_piece(clicked_piece)
            elif clicked_piece is not None and clicked_piece.color == Color.BLACK and not chess_board.is_white_turn:
                chess_board.draw_possible_moves(screen, clicked_piece)
                chess_board.set_selected_piece(clicked_piece)

    # Update the chess board
    chess_board.draw(screen)

    # checkmate
    chess_board.update_kings()
    if chess_board.checkmate(Color.WHITE):
        print("Black wins!")
        running = False
    elif chess_board.checkmate(Color.BLACK):
        print("White wins!")
        running = False

    # Draw the chess board
    screen.fill((0, 0, 0))  # Fill the screen with black
    chess_board.draw(screen)
    pygame.display.flip()  # Update the full display surface

# Done! Time to quit.
pygame.quit()
