from chess.models import Cell
from chess.models.cards.card import Card


class ActionCard(Card):
    def __init__(self, costs: int):
        super().__init__(costs)

    def get_actions(self, pos: Cell, board: 'AoWBoard', turn: int) -> tuple:
        """
        Get the actions of the card
        @param pos: Cell: The position of the card
        @param board: AoWBoard: The board of the game
        @param turn: int: The turn of the game
        @return: tuple: The actions of the card
        """
        raise NotImplementedError("This method must be implemented by the subclass")

    def play(self, pos: Cell, board: 'AoWBoard', turn: int) -> None:
        """
        Play the card
        @param pos: Cell: The position of the card
        @param board: AoWBoard: The board of the game
        @param turn: int: The turn of the game
        @return: None
        """
        raise NotImplementedError("This method must be implemented by the subclass")

