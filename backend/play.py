import os
import sys

import numpy as np
import pygame
from dotenv import load_dotenv

from agents import PlayAgent
from aow.game.aow import ArtOfWar
from buffer.episode import Episode
from learnings.ppo import PPO

load_dotenv()

sys.setrecursionlimit(int(os.getenv("RECURSION_LIMIT")))
env = ArtOfWar(window_size=int(os.getenv("AOW_WINDOW_SIZE")), max_steps=int(os.getenv("AOW_MAX_STEPS")))

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
try:
    ppo_aow = PlayAgent(env, ppo, episodes=int(os.getenv("EPISODES")), train_on=int(os.getenv("BUFFER_SIZE")),
                        result_folder="", white_ppo_path=white_ppo_path, black_ppo_path=black_ppo_path)
except FileNotFoundError:
    print("Could not find model on specified location, make sure the location is correct."
          " If you have not trained a model yet, train one first.")
    sys.exit()

env.render()
ep = Episode()
running = True
counter = 0
while running:
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
            running = False
            break
    turn = env.aow_logic.turn
    if turn == 0:
        action_str = input("Choose action (e.g., 'e2e4'): ")

        if action_str == 'q':
            break

        # Convert human-readable action to aow move object
        try:
            f1 = int(action_str[1]) - 1
            f2 = ord(action_str[0]) - ord('a')
            from_pos = np.array([f1, f2])
            t1 = int(action_str[3]) - 1
            t2 = ord(action_str[2]) - ord('a')
            to_pos = np.array([t1, t2])

            src, dst, mask = env.aow_logic.get_all_actions(turn)
            action = np.where((src == from_pos).all(axis=1) & (dst == to_pos).all(axis=1))[0]

            # getting all valid actions for the piece
            all_possible_actions_for_piece = np.where((src == from_pos).all(axis=1))[0]
            all_playable_actions_for_piece = []
            for i in all_possible_actions_for_piece:
                if mask[i] == 1:
                    all_playable_actions_for_piece.append(i)
            all_playable_actions_for_piece = np.array(all_playable_actions_for_piece)

            print("Possible actions:")
            for i in all_possible_actions_for_piece:
                to_loc = dst[i]
                from_loc = src[i]
                string_to = chr(to_loc[1] + ord('a')) + str(to_loc[0] + 1)
                string_from = chr(from_loc[1] + ord('a')) + str(from_loc[0] + 1)
                print(f"{src[i]} -> {dst[i]} or {string_from} -> {string_to}")
            print("Possible actions:")
            for i in all_playable_actions_for_piece:
                to_loc = dst[i]
                from_loc = src[i]
                string_to = chr(to_loc[1] + ord('a')) + str(to_loc[0] + 1)
                string_from = chr(from_loc[1] + ord('a')) + str(from_loc[0] + 1)
                print(f"{src[i]} -> {dst[i]} or {string_from} -> {string_to}")

            if len(action) == 0:
                print("Invalid action")
                continue

            print(f"Action = {action}", src[action], dst[action])
            action = action[0]
            rewards, done, infos = env.step(action)
            print(f"Rewards = {rewards}")
            print(f"Infos = {infos}")
            print("-" * 64)
        except Exception as e:
            print(e)
            print("Invalid action")
            continue

        env.render()
        action_str = ''
    else:
        print("White" if turn else "Black")
        done, _ = ppo_aow.take_action(turn, ep)

        rewards = ep.rewards
        print("turn: ", counter)
        print(f"Rewards = {rewards}")
        print("-" * 64)
        env.render()
    if done:
        env.reset()
        print("RESET")

env.close()
