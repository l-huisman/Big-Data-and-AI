from fastapi import HTTPException

from agents import PPOChess
from api.models.requests import AIGameRequest
from api.models.responses import AIGameResponse
from api.routes.base import BaseRoute
from buffer.episode import Episode
from chess.constants.info_keys import CHECK_MATE_WIN


class AiGame(BaseRoute):
    def __init__(self, env, ai_game_request: AIGameRequest):
        super().__init__(env)
        self.ai_game_request = ai_game_request

    def execute(self):
        try:
            self.logger.info(f"Received ai game request: {self.ai_game_request}")
            self.reset_environment()
            agent = self.get_agent(black_model_name=self.ai_game_request.black_model,
                                   white_model_name=self.ai_game_request.white_model)
            return self.play_game(agent=agent, episode=Episode())
        except HTTPException as e:
            raise e
        except FileNotFoundError as e:
            self.logger.error(f"Could not find model on specified location, make sure the location is correct. {e}")
            raise self.raise_http_exception(status_code=500, detail="Could not find any model.")
        except Exception as e:
            self.logger.error(f"An error occurred while resetting the game. {e}")
            raise self.raise_http_exception(status_code=500, detail="An error occurred while initializing the game.")

    def get_agent(self, white_model_name: str = "PPO", black_model_name: str = "PPO"):
        match white_model_name.capitalize():
            case "PPO":
                white_model = self.WHITE_PPO_PATH
            case "DQN":
                white_model = self.WHITE_DQN_PATH
            case "A2C":
                white_model = self.WHITE_A2C_PATH
            case _:
                white_model = self.WHITE_PPO_PATH

        match black_model_name.capitalize():
            case "PPO":
                black_model = self.BLACK_PPO_PATH
            case "DQN":
                black_model = self.BLACK_DQN_PATH
            case "A2C":
                black_model = self.BLACK_A2C_PATH
            case _:
                black_model = self.BLACK_PPO_PATH

        return PPOChess(self.env, self.get_ppo(), 1, 32, "", white_model, black_model)

    def play_game(self, agent, episode) -> AIGameResponse:
        response = AIGameResponse(game=[], statistics=[], possibles=[], source_pos=[], action_mask=[], winner="")

        response.game.append(agent.env.aow_board.get_numeric_board().tolist())
        response.statistics.append({"rewards": [0, 0], "infos": [[], []], "end": False})

        done = False
        info = None
        while not done:
            done, info = agent.take_action(agent.env.aow_logic.turn, episode)
            response.statistics.append({"rewards": info[1], "infos": info[7], "end": done})
            response.game.append(agent.env.aow_board.get_numeric_board().tolist())

        response = self.check_winner(info[7], response)
        self.logger.info("AI game completed.")
        return response
    
    def check_winner(self, info, response):
        if CHECK_MATE_WIN in info[0]:
            response.winner = "White"
        elif CHECK_MATE_WIN in info[1]:
            response.winner = "Black"
        elif CHECK_MATE_WIN not in info[0] and CHECK_MATE_WIN not in info[1]:
            response.winner = "Draw"
        return response
