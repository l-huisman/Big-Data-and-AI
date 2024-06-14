import os
import sys
from time import sleep

import pygame
from dotenv import load_dotenv

from agents import PlayAgent
from aow.game.aow import ArtOfWar
from buffer.episode import Episode
from learnings.ppo import PPO

load_dotenv()

sys.setrecursionlimit(int(os.getenv("RECURSION_LIMIT")))
env = ArtOfWar(window_size=int(os.getenv("AOW_WINDOW_SIZE")), max_steps=int(os.getenv("AOW_MAX_STEPS")))
env.render()

# Paths to your trained api
white_ppo_path = os.getenv("PPO_RESULT_FOLDER") + '/white_dict.pt'
black_ppo_path = os.getenv("PPO_RESULT_FOLDER") + '/black_dict.pt'

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

# Create an instance of PlayAgent
aow_game = PlayAgent(env, ppo, episodes=int(os.getenv("EPISODES")), train_on=int(os.getenv("BUFFER_SIZE")),
                        result_folder="", white_ppo_path=white_ppo_path, black_ppo_path=black_ppo_path)

episode = Episode()
# Play the game
counter = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    done, _ = aow_game.take_action(aow_game.env.aow_logic.turn, episode)
    # print("turn: ", aow_game.env.turn)
    env.render()
    sleep(.1)  # Pause for a short time to make the game viewable
    counter += 1
    if done:
        print("Game Over")
        print("Winner: White" if aow_game.env.aow_logic.turn else "Winner: Black")
        print("Game Length: ", counter)
        break
