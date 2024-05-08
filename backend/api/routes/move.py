import logging

import numpy as np
from fastapi import HTTPException

from api.models.requests import MoveRequest
from api.models.responses import MoveResponse
from utils import raise_http_exception, validate_board_size, matches_regex, reverse_move, convert_move_to_positions

logger = logging.getLogger(__name__)

# TODO: make nice
def move(move_request: MoveRequest, env, agent, episode):
    logger.info(f"Received move request: {move_request}")
    try:
        env.reset()
    except Exception as e:
        logger.error(f"An error occurred while resetting the game. {e}")
        raise raise_http_exception(500, detail="An error occurred while resetting the game.")

    if agent is None:
        logger.error("No game has been initialized yet.")
        raise_http_exception(404, "No game has been initialized yet.")

    board: np.ndarray | None = None
    try:
        board = np.array(move_request.board)
        if not board.any():
            raise_http_exception(400, "Please provide a board.")
    except Exception as e:
        logger.warning(f"An error occurred while processing the board. {e}")
        raise_http_exception(400, "Invalid board.")

    validate_board_size(board)

    env.set_board(board)
    env.turn = move_request.turn
    action_str = move_request.move

    # check if the move is in the correct format
    if not matches_regex(action_str, r"^[a-h][1-8][a-h][1-8]$"):
        raise_http_exception(400,
                             "Move does not have the correct format."
                             " Please provide a move in the format of \"a1a2\".")

    player_move_board = []
    try:
        # if the turn is 1, reverse the move (e7e5 -> e2e4)
        if env.turn == 1:
            action_str = reverse_move(action_str)

        # - TODO: Check error's thrown and make handling those better
        from_pos, to_pos = convert_move_to_positions(action_str)
        src, dst, _ = env.get_all_actions(env.turn)
        action = np.nonzero((src == from_pos).all(axis=1) & (dst == to_pos).all(axis=1))[0]
        if len(action) == 0:
            raise_http_exception(400, "Invalid move.")
        _, done, _ = env.step(int(action[0]))

        player_move_board = env.board.tolist()

        if done:
            return MoveResponse(playerMoveBoard=player_move_board, CombinedMoveBoard=player_move_board, cards=[],
                                resources=0, has_game_ended=done)
    except HTTPException as e:
        logger.warning(f"An error occurred while processing the move. {e}")
        raise e
    except Exception as e:
        logger.warning("Something went wrong while processing the move. " + str(e))
        raise_http_exception(400, "Invalid move")

    try:
        agent.take_action(env.turn, episode)
    except Exception as e:
        logger.error(f"An error occurred while processing the AI's move. {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the AI's move.")

    logger.info("Move processed successfully.")
    return MoveResponse(playerMoveBoard=player_move_board, CombinedMoveBoard=env.board.tolist(), cards=[], resources=0,
                        has_game_ended=env.done)
