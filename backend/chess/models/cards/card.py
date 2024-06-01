
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

    def get_cost(self) -> int:
        """
        Get the cost of the card
        :return: int: The cost of the card
        """
        return self.costs


