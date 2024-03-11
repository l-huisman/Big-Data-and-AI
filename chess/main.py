import pygame
from board import Board

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = (640, 640)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a chess board
chess_board = Board()

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

    # Update the chess board
    chess_board.draw(screen)

    # Draw the chess board
    screen.fill((0, 0, 0))  # Fill the screen with black
    chess_board.draw(screen)
    pygame.display.flip()  # Update the full display surface

# Done! Time to quit.
pygame.quit()
