import pygame
from constants import Color


class Piece:
    def __init__(
        self,
        board,
        color: Color,
        x_position: int,
        y_position: int,
    ):
        self.moves = []
        self.board = board
        self.color = color
        self.x_position = x_position
        self.y_position = y_position
        self._legal_moves = []
        self.__has_moved = False

    def get_possible_moves(self) -> list:
        raise NotImplementedError

    def draw(self, screen, square_size: int, y: int, x: int) -> None:
        image = pygame.image.load(
            "chess/img/" + self.__class__.__name__ + "_" + self.color.name + ".png"
        )
        image = pygame.transform.scale(image, (square_size, square_size))
        screen.blit(image, (x * square_size, y * square_size))

    def _check_legal_moves(self) -> None:
        for move in self._legal_moves:
            x = self.x_position + move[0]
            y = self.y_position + move[1]
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            piece_at_position = self.board.get_piece_at_position(x, y)
            if piece_at_position == None:
                self.moves.append((x, y))
            elif piece_at_position.color != self.color:
                self.moves.append((x, y))

    def _check_straights(self, x_increment, y_increment) -> None:
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

    def get_has_moved(self) -> bool:
        return self.__has_moved

    def set_has_moved(self) -> bool:
        self.__has_moved = True

    def get_position(self) -> tuple:
        return (self.x_position, self.y_position)

    def set_position(self, x: int, y: int) -> None:
        self.x_position = x
        self.y_position = y
