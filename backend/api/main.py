import logging
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents import PPOChess
from api.models.requests import MoveRequest, AIGameRequest, ActionRequest
from api.models.responses import AIGameResponse, InitializeResponse, MoveResponse, ActionResponse
from api.routes import Move, PlayableActions, Initialize, AiGame
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


@app.get(path="/initialize", response_model=InitializeResponse)
def initialize():
    route = Initialize.Initialize(env=env)
    return route.execute()


@app.post(path="/move", response_model=MoveResponse)
def move(move_request: MoveRequest):
    route = Move.Move(env=env, agent=ppo_chess, episode=episode, move_request=move_request)
    return route.execute()


@app.get(path="/actions", response_model=ActionResponse)
def actions(action_request: ActionRequest):
    route = PlayableActions.PlayableActions(env=env, action_request=action_request)
    return route.execute()


@app.post(path="/aigame", response_model=AIGameResponse)
def aigame(ai_game_request: AIGameRequest):
    route = AiGame.AiGame(env=env, ai_game_request=ai_game_request)
    return route.execute()
