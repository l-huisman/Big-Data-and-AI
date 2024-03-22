from .piece import Piece
from constants import Color
from .rook import Rook


class King(Piece):
    def __init__(self, board, color: Color, x_position: int, y_position: int):
        super().__init__(board, color, x_position, y_position)
        self._legal_moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def get_possible_moves(self):
        self.moves = []
        self._check_legal_moves()
        self._check_castling()
        return self.moves
    
    def _check_castling(self):
        #Check if the king has moved
        if self.get_has_moved():
            return
        
        # Check for castling on the right
        castlingRight = True
        for i in range(1, 3):
            piece_at_position = self.board.get_piece_at_position(self.x_position + i, self.y_position)
            if piece_at_position != None:
                castlingRight = False
        
        if castlingRight:
            # Check the rook when castling on the right
            rook = self.board.get_piece_at_position(self.x_position + 3, self.y_position)
            if isinstance(rook, Rook) and not rook.get_has_moved():
                self.moves.append((self.x_position + 2, self.y_position))
        
        # Check for castling on the left
        castlingLeft = True
        for i in range(1, 4):
            piece_at_position = self.board.get_piece_at_position(self.x_position - i, self.y_position)
            if piece_at_position != None:
                castlingLeft = False
        
        if castlingLeft:
            # Check the rook when castling on the left
            rook = self.board.get_piece_at_position(self.x_position - 4, self.y_position)
            if isinstance(rook, Rook) and not rook.get_has_moved():
                self.moves.append((self.x_position - 2, self.y_position))
