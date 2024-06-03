import csv
from chess.game.aow import ArtOfWar
import sys

from agents import PPOChess
from buffer.episode import Episode
from learnings.ppo import PPO

sys.setrecursionlimit(300)
env = ArtOfWar(window_size=800, max_steps=128)
# env.render()

# Paths to your trained api
white_ppo_path = 'results/DoubleAgentsPPO/white_dict.pt'
black_ppo_path = 'results/DoubleAgentsPPO/black_dict.pt'

ppo = PPO(
    env,
    hidden_layers=(2048,) * 4,
    epochs=100,
    buffer_size=32 * 2,
    batch_size=128,
)

mydict = []

for i in range(100):
    env.reset()
    chess_game = PPOChess(env, ppo, 1, 32, "", white_ppo_path, black_ppo_path)
    # Create an instance of PPOChess

    episode = Episode()
    # Play the game
    counter = 0

    states = []

    states.append(chess_game.env.get_state(chess_game.env.turn))

    while True:
        done, _ = chess_game.take_action(chess_game.env.turn, episode)
        states.append(chess_game.env.get_state(chess_game.env.turn))

        # print("turn: ", chess_game.env.turn)
        # env.render()
        counter += 1
        if done:
            # GameStates | Win -1 of 1 | nr turns | nr checks
            data = {'States': states, 'Win': chess_game.env.turn, 'Turns': counter}
            mydict.append(data)

            print("Game Over")
            print("Winner: White" if chess_game.env.turn else "Winner: Black")
            print("Game Length: ", counter)
            break

# field names
fields = ['States', 'Win', 'Turns']

# writing to csv file
with open('gamedata.csv', 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    # writing headers (field names)
    writer.writeheader()

    # writing data rows
    writer.writerows(mydict)
