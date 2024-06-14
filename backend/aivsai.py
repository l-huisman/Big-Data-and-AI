import sys
from time import sleep

import pygame

from agents import PlayAgent
from buffer.episode import Episode
from aow.game.aow import ArtOfWar
from learnings.ppo import PPO

sys.setrecursionlimit(300)
env = ArtOfWar(window_size=800, max_steps=256)
env.render()

# Paths to your trained api
white_ppo_path = 'results/DoubleAgentsPPO/white_dict.pt'
black_ppo_path = 'results/DoubleAgentsPPO/black_dict.pt'

ppo = PPO(
    env,
    hidden_layers=(2048,) * 4,
    epochs=100,
    buffer_size=32 * 2,
    batch_size=256,
)

# dqn = DQNLearner(
#     env,
#     epochs=100,
#     gamma=0.99,
#     learning_rate=0.003,
#     hidden_layers=(2048,) * 4,
#     buffer_size=32,
#     batch_size=128,
#     epsilon=0.1,
#     epsilon_decay=0.995,
#     epsilon_min=0.01,
#     tau=0.99,
#     update_every=4,
# )

# Create an instance of PlayAgent
aow_game = PlayAgent(env, ppo, 1, 32, "", white_ppo_path, black_ppo_path)

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
