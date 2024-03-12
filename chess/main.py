import pygame
from board import Board

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
def get_mouse_position(mouse_pos: tuple) -> tuple:
    x = mouse_pos[0] // 80
    y = mouse_pos[1] // 80
    return x, y


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
        # Check for mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            mouse_pos = pygame.mouse.get_pos()
            x, y = get_mouse_position(mouse_pos)

            # Check if the clicked position is a valid move for the selected piece
            if chess_board.get_selected_piece() is not None:
                if (x, y) in chess_board.get_selected_piece().get_possible_moves():
                    piece = chess_board.get_selected_piece()
                    chess_board.move_piece(piece.get_position(), (x, y))
                    chess_board.set_selected_piece(None)
                    piece.set_position(x, y)
            else:
                clicked_piece = chess_board.get_piece_at_position(x, y)
                if clicked_piece is not None:
                    chess_board.draw_possible_moves(screen, clicked_piece)
                    chess_board.set_selected_piece(clicked_piece)
                else:
                    chess_board.set_selected_piece(None)

    # Update the chess board
    chess_board.draw(screen)

    # Draw the chess board
    screen.fill((0, 0, 0))  # Fill the screen with black
    chess_board.draw(screen)
    pygame.display.flip()  # Update the full display surface

# Done! Time to quit.
pygame.quit()
