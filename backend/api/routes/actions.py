import logging

import numpy as np

from api.models.requests import ActionRequest
from api.models.responses import ActionResponse
from chess import Chess
from utils import convert_cell_to_position, raise_http_exception

logger = logging.getLogger(__name__)

# TODO: make nice
def get_playable_actions(action_request: ActionRequest, env: Chess) -> ActionResponse:
    logger.info(f"Received action request: {action_request}")
    try:
        env.reset()
    except Exception as e:
        logger.error(f"An error occurred while resetting the game. {e}")
        raise raise_http_exception(500, detail="An error occurred while resetting the game.")

    try:
        src, dst, mask = env.get_all_actions(action_request.turn)
        from_pos = convert_cell_to_position(action_request.pieceLocation)

        # getting all valid actions for the piece
        all_possible_actions_for_piece = np.where((src == from_pos).all(axis=1))[0]
        all_playable_actions_for_piece = []
        for i in all_possible_actions_for_piece:
            if mask[i] == 1:
                all_playable_actions_for_piece.append(i)
        all_playable_actions_for_piece = np.array(all_playable_actions_for_piece)
        playable_moves = []
        print("Possible actions:")
        for i in all_playable_actions_for_piece:
            to_loc = dst[i]
            from_loc = src[i]
            string_to = chr(to_loc[1] + ord('a')) + str(to_loc[0] + 1)
            string_from = chr(from_loc[1] + ord('a')) + str(from_loc[0] + 1)
            playable_moves.append(f"{string_from}{string_to}")
        return ActionResponse(possibleMoves=playable_moves)
    except Exception as e:
        logger.error(f"An error occurred while getting the possible moves. {e}")
        raise raise_http_exception(500, detail="An error occurred while getting the possible moves.")
    finally:
        logger.info("Action request completed.")
