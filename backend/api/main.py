import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

from agents import PlayAgent
from api.models.requests import MoveRequest, AIGameRequest, ActionRequest
from api.models.responses import AIGameResponse, InitializeResponse, MoveResponse, ActionResponse
from api.routes import Move, PlayableActions, Initialize, AiGame
from buffer.episode import Episode
from aow.game.aow import ArtOfWar
from learnings.ppo import PPO

load_dotenv()

WHITE_PPO_PATH = os.getenv("PPO_RESULT_FOLDER") + '/white_dict.pt'
BLACK_PPO_PATH = os.getenv("PPO_RESULT_FOLDER") + '/black_dict.pt'
WHITE_DQN_PATH = os.getenv("DQN_RESULT_FOLDER") + '/white_dict.pt'
BLACK_DQN_PATH = os.getenv("DQN_RESULT_FOLDER") + '/black_dict.pt'

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
env = ArtOfWar(window_size=800, max_steps=256)

ppo = PPO(
    env,
    hidden_layers=(int(os.getenv("PPO_HIDDEN_LAYERS_SIZE")),) * int(os.getenv("PPO_HIDDEN_LAYERS_COUNT")),
    epochs=int(os.getenv("PPO_EPOCHS")),
    buffer_size=int(os.getenv("BUFFER_SIZE")) * 2,
    batch_size=int(os.getenv("BATCH_SIZE")),
    gamma=float(os.getenv("PPO_GAMMA")),
    gae_lambda=float(os.getenv("PPO_GAE_LAMBDA")),
    policy_clip=float(os.getenv("PPO_POLICY_CLIP")),
    learning_rate=float(os.getenv("PPO_LEARNING_RATE")),
)

episode = Episode()
ppo_aow = None
try:
    ppo_aow = PlayAgent(env, ppo, episodes=int(os.getenv("EPISODES")), train_on=int(os.getenv("BUFFER_SIZE")),
                        result_folder="", white_ppo_path=WHITE_PPO_PATH, black_ppo_path=BLACK_PPO_PATH)
except Exception as e:
    logger.error(e)
    raise Exception("Failed to initialize aow agent. Try training (or retraining) the model.")


@app.get(path="/initialize", response_model=InitializeResponse)
def initialize():
    route = Initialize.Initialize(env=env)
    return route.execute()


@app.post(path="/move", response_model=MoveResponse)
def move(move_request: MoveRequest):
    route = Move.Move(env=env, agent=ppo_aow, episode=episode, move_request=move_request)
    return route.execute()


@app.post(path="/actions", response_model=ActionResponse)
def actions(action_request: ActionRequest):
    route = PlayableActions.PlayableActions(env=env, action_request=action_request)
    return route.execute()


@app.post(path="/aigame", response_model=AIGameResponse)
def aigame(ai_game_request: AIGameRequest):
    route = AiGame.AiGame(env=env, ai_game_request=ai_game_request)
    return route.execute()
