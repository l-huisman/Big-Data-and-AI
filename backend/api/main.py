import logging
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents import PPOChess
from api.models.requests import MoveRequest, AIGameRequest, ActionRequest
from api.models.responses import AIGameResponse
from api.routes.initialize import initialize as initialize_action
from api.routes.actions import get_playable_actions
from api.routes.move import move as move_action
from buffer.episode import Episode
from chess import Chess
from learnings.ppo import PPO

WHITE_PPO_PATH = 'results/DoubleAgentsPPO/white_dict.pt'
BLACK_PPO_PATH = 'results/DoubleAgentsPPO/black_dict.pt'
WHITE_DQN_PATH = 'results/DoubleAgentsDQN/white_dict.pt'
BLACK_DQN_PATH = 'results/DoubleAgentsDQN/black_dict.pt'

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename='./api.log',
                    format='%(asctime)s|%(name)s:%(levelname)s - %(message)s')
logger.info("API started.")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sys.setrecursionlimit(300)
env = Chess(window_size=800)

ppo = PPO(
    env,
    hidden_layers=(2048,) * 4,
    epochs=100,
    buffer_size=32 * 2,
    batch_size=128,
)

episode = Episode()
ppo_chess = PPOChess(env, ppo, 1, 32, "", WHITE_PPO_PATH, BLACK_PPO_PATH)


@app.get("/initialize", status_code=201)
def initialize():
    return initialize_action(env)


@app.post("/move")
def move(move_request: MoveRequest):
    return move_action(move_request, env, ppo_chess, episode)


@app.get("/actions")
def actions(action_request: ActionRequest):
    return get_playable_actions(action_request, env)

@app.post("/aigame", status_code=201)
def aigame(aigame_request: AIGameRequest):
    logger.info(f"Received aigame request: {aigame_request}")
    response = AIGameResponse(game=[], statistics=[])
    try:
        env.reset()

        match aigame_request.white_model.capitalize():
            case "PPO":
                white_model = WHITE_PPO_PATH
            case "DQN":
                # white_model = WHITE_DQN_PATH
                logger.info("DQN not implemented yet, using PPO instead.")
                white_model = WHITE_PPO_PATH
            case _:
                white_model = WHITE_PPO_PATH

        match aigame_request.black_model.capitalize():
            case "PPO":
                black_model = BLACK_PPO_PATH
            case "DQN":
                # black_model = BLACK_DQN_PATH
                logger.info("DQN not implemented yet, using PPO instead.")
                black_model = BLACK_PPO_PATH
            case _:
                black_model = BLACK_PPO_PATH

        ppo_chess = PPOChess(env, ppo, 1, 32, "", white_model, black_model)
        episode = Episode()
        logger.info("Initialized AI game.")

        # Play the game
        counter = 0
        response.game.append(ppo_chess.env.board.tolist())
        response.statistics.append({"rewards": [0, 0], "infos": [[], []], "end": False})

        while True:
            done, _ = ppo_chess.take_action(ppo_chess.env.turn, episode)
            response.statistics.append({"rewards": _[1], "infos": _[7], "end": done})
            response.game.append(ppo_chess.env.board.tolist())

            counter += 1
            if done:
                logger.info("Game Over")
                logger.info("Winner: White" if ppo_chess.env.turn else "Winner: Black")
                logger.info("Game Length: ", counter)
                break

        logger.info(f"AI game completed.")
        return response
    except FileNotFoundError as e:
        logger.error(f"Could not find model on specified location, make sure the location is correct. {e}")
        raise HTTPException(status_code=500, detail="Could not find any model.")
    except Exception as e:
        logger.error(f"An error occurred while resetting the game. {e}")
        raise HTTPException(status_code=500, detail="An error occurred while initializing the game.")
