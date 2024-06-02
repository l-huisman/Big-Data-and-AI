from chess.models import Cell


class Card:
    def __init__(self, costs: int):
        self.played = False
        self.costs = costs

    def is_played(self) -> bool:
        """
        Check if the card has been played
        :return: int: If card has been played
        """
        return self.played

    def set_played(self, played: bool = True) -> None:
        """
        Set the card to played
        """
        self.played = played

    def get_cost(self) -> int:
        """
        Get the cost of the card
        :return: int: The cost of the card
        """
        return self.costs

    def get_actions(self, pos: Cell, board: 'AoWBoard', turn: int) -> tuple:
        """
        Get the actions of the card
        @param pos: Cell: The position of the card
        @param board: AoWBoard: The board of the game
        @param turn: int: The turn of the game
        @return: tuple: The actions of the card
        """
        raise NotImplementedError("This method must be implemented by the subclass")
