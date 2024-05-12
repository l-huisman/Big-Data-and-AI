import numpy as np

from api.models.requests import ActionRequest
from api.models.responses import ActionResponse
from api.routes.base import BaseRoute
from chess import Chess
from utils import convert_cell_to_position


class PlayableActions(BaseRoute):
    def __init__(self, env: Chess, action_request: ActionRequest):
        super().__init__(env)
        self.action_request = action_request

    def execute(self) -> ActionResponse:
        self.logger.info(f"Received action request: {self.action_request}")

        try:
            src, dst, mask = self.env.get_all_actions(self.action_request.turn)
            from_pos = convert_cell_to_position(self.action_request.pieceLocation)

            # getting all valid actions for the piece
            all_possible_actions_for_piece = np.where((src == from_pos).all(axis=1))[0]
            all_playable_actions_for_piece = []
            for i in all_possible_actions_for_piece:
                if mask[i] == 1:
                    all_playable_actions_for_piece.append(i)
            all_playable_actions_for_piece = np.array(all_playable_actions_for_piece)
            playable_moves = []
            self.logger.info("Possible actions:")
            for i in all_playable_actions_for_piece:
                to_loc = dst[i]
                from_loc = src[i]
                string_to = chr(to_loc[1] + ord('a')) + str(to_loc[0] + 1)
                string_from = chr(from_loc[1] + ord('a')) + str(from_loc[0] + 1)
                playable_moves.append(f"{string_from}{string_to}")
            return ActionResponse(possibleMoves=playable_moves)
        except Exception as e:
            self.logger.error(f"An error occurred while getting the possible moves. {e}")
            self.raise_http_exception(500, detail="An error occurred while getting the possible moves.")
        finally:
            self.logger.info("Action request completed.")
