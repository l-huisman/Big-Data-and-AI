import numpy as np

from api.models.requests import ActionRequest
from api.models.responses import ActionResponse
from api.routes.base import BaseRoute
from chess.game.aow import ArtOfWar
from utils import convert_cell_to_position


class PlayableActions(BaseRoute):
    def __init__(self, env: ArtOfWar, action_request: ActionRequest):
        super().__init__(env)
        self.action_request = action_request

    def execute(self) -> ActionResponse:
        self.logger.info(f"Received action request: {self.action_request}")

        try:
            src, dst, mask = self.env.get_all_actions(self.action_request.turn)
            from_pos = self.convert_cell_to_position()

            all_playable_actions_for_piece = self.get_all_playable_actions_for_piece(src, from_pos, mask)
            formatted_playable_moves = self.format_playable_moves(all_playable_actions_for_piece, src, dst)

            return ActionResponse(possibleMoves=formatted_playable_moves)
        except Exception as e:
            self.logger.error(f"An error occurred while getting the possible moves. {e}")
            self.raise_http_exception(500, detail="An error occurred while getting the possible moves.")
        finally:
            self.logger.info("Action request completed.")

    def convert_cell_to_position(self):
        return convert_cell_to_position(self.action_request.pieceLocation)

    @staticmethod
    def get_all_playable_actions_for_piece(src, from_pos, mask):
        all_possible_actions_for_piece = np.nonzero((src == from_pos).all(axis=1))[0]
        all_playable_actions_for_piece = []
        for i in all_possible_actions_for_piece:
            if mask[i] == 1:
                all_playable_actions_for_piece.append(i)
        return np.array(all_playable_actions_for_piece)

    @staticmethod
    def format_playable_moves(all_playable_actions_for_piece, src, dst):
        playable_moves = []
        for i in all_playable_actions_for_piece:
            to_loc = dst[i]
            from_loc = src[i]
            string_to = chr(to_loc[1] + ord('a')) + str(to_loc[0] + 1)
            string_from = chr(from_loc[1] + ord('a')) + str(from_loc[0] + 1)
            playable_moves.append(f"{string_from}{string_to}")
        return playable_moves
