from api.models.responses import InitializeResponse
from api.routes.base import BaseRoute
from chess.game.aow import ArtOfWar


class Initialize(BaseRoute):
    def __init__(self, env: ArtOfWar):
        super().__init__(env)

    def execute(self) -> InitializeResponse:
        self.logger.info("Received initialize request.")
        try:
            self.env.reset()

            cards = self.env.aow_board.get_cards(0)
            card_names = []
            for card in cards:
                card_names.append(card.__str__())
            return InitializeResponse(board=self.env.aow_board.get_numeric_board().tolist(), cards=card_names,
                                      resources=self.env.aow_board.resources, pieces=self.env.aow_board.pieces)
        except FileNotFoundError as e:
            self.logger.error(f"Could not find model on specified location, make sure the location is correct. {e}")
            self.raise_http_exception(status_code=500, detail="Could not find any model.")
        except Exception as e:
            self.logger.error(f"An error occurred while resetting the game. {e}")
            self.raise_http_exception(status_code=500, detail="An error occurred while initializing the game.")
        finally:
            self.logger.info("Initialized game.")
