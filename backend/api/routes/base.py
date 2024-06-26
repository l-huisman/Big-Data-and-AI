import logging
import os
from dotenv import load_dotenv

from fastapi import HTTPException

from learnings.ppo import PPO
from utils import matches_regex

BOARD_LENGTH = 8
BOARD_WIDTH = 8
BOARD_SIDES = 2

load_dotenv()

class BaseRoute:
    def __init__(self, env):
        self.logger = logging.getLogger(__name__)
        self.env = env

    WHITE_PPO_PATH = os.getenv("PPO_RESULT_FOLDER") + '/white_dict.pt'
    BLACK_PPO_PATH = os.getenv("PPO_RESULT_FOLDER") + '/black_dict.pt'
    WHITE_DQN_PATH = os.getenv("DQN_RESULT_FOLDER") + '/white_dict.pt'
    BLACK_DQN_PATH = os.getenv("DQN_RESULT_FOLDER") + '/black_dict.pt'
    WHITE_A2C_PATH = os.getenv("A2C_RESULT_FOLDER") + '/white_dict.pt'
    BLACK_A2C_PATH = os.getenv("A2C_RESULT_FOLDER") + '/black_dict.pt'

    def execute(self):
        raise NotImplementedError()

    def validate_regex(self, string, regex, http_response_message) -> None:
        if not matches_regex(string, regex):
            self.raise_http_exception(status_code=400, detail=http_response_message)

    @staticmethod
    def raise_http_exception(status_code, detail):
        raise HTTPException(status_code=status_code, detail=detail)

    def validate_board_size(self, board):
        if len(board) != BOARD_SIDES:
            self.raise_http_exception(400, f"Invalid board size. ({len(board)}) should be {BOARD_SIDES}.")
        if len(board[0]) != BOARD_WIDTH or len(board[1]) != BOARD_WIDTH:
            self.raise_http_exception(400,
                                      f"Invalid board size. ({len(board[0])}, {len(board[1])}) should be {BOARD_WIDTH},"
                                      f" {BOARD_WIDTH}")
        for row in board[0]:
            if len(row) != BOARD_LENGTH:
                self.raise_http_exception(400, f"Invalid board size. ({len(row)}) should be {BOARD_LENGTH}")
        for row in board[1]:
            if len(row) != BOARD_LENGTH:
                self.raise_http_exception(400, f"Invalid board size. ({len(row)}) should be {BOARD_LENGTH}")

    def reset_environment(self):
        try:
            self.env.reset()
        except Exception as e:
            self.logger.error(f"An error occurred while resetting the game. {e}")
            raise self.raise_http_exception(500, detail="An error occurred while resetting the game.")

    def get_ppo(self):
        return PPO(
            self.env,
            hidden_layers=(int(os.getenv("PPO_HIDDEN_LAYERS_SIZE")),) * int(os.getenv("PPO_HIDDEN_LAYERS_COUNT")),
            epochs=int(os.getenv("PPO_EPOCHS")),
            buffer_size=int(os.getenv("BUFFER_SIZE")) * 2,
            batch_size=int(os.getenv("BATCH_SIZE")),
            gamma=float(os.getenv("PPO_GAMMA")),
            gae_lambda=float(os.getenv("PPO_GAE_LAMBDA")),
            policy_clip=float(os.getenv("PPO_POLICY_CLIP")),
            learning_rate=float(os.getenv("PPO_LEARNING_RATE")),
        )
