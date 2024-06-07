import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

A = 0.25
B = "tab:blue"
W = "tab:orange"

ALPHA = 0.25
COUNT = 512  # 512
for name in ["Double AgentsPPO", "Double AgentsDQN", "Single Agent", "Double AgentsA2C"]:
    print(name, "...")
    folder = "".join(name.split(" "))
    folder = f"results/{folder}"
    moves = np.load(f"{folder}/moves.npy")
    mates = np.load(f"{folder}/mates_win.npy")
    checks = np.load(f"{folder}/checks_win.npy")
    rewards = np.load(f"{folder}/rewards.npy")
    episodes = np.max(np.where(moves[0] != 0)) + 1

    white_rewards = rewards[1, :episodes]
    plt.figure(figsize=(10, 6), dpi=200)
    plt.plot(white_rewards, label="White Rewards")
    plt.title("Average Rewards for White")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.legend()
    plt.grid()
    plt.savefig(f"{folder}/white_rewards.jpeg")
    
    black_rewards = rewards[0, :episodes]
    plt.figure(figsize=(10, 6), dpi=200)
    plt.plot(black_rewards, label="Black Rewards")
    plt.title("Average Rewards for Black")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.legend()
    plt.grid()
    plt.savefig(f"{folder}/black_rewards.jpeg")



ppochecks = np.load("results/DoubleAgentsPPO/checks_win.npy")
a2cchecks = np.load("results/DoubleAgentsA2C/checks_win.npy")
moves = np.load("results/DoubleAgentsPPO/moves.npy")

def density(arr, count, episode):
    a = arr.max(axis=0)
    return [np.sum(a[max(0, i - count) : i]) / count for i in range(episode)]


def plot_check_mates(
    ax, check_mates_arr: np.ndarray, episodes: int, count_density: int
):
    #     ax.plot(check_mates_arr.max(axis=0)[:episodes], alpha=0.25)
    density_ax = ax.twinx()
    density_arr = density(check_mates_arr, count_density, episodes)
    density_ax.plot(
        range(episodes),
        density_arr,
        color="tab:green",
        alpha=1,
        label=f"total check mates rate for {count_density} episodes",
        linewidth=2,
    )
    density_ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    density_ax.legend()
    density_ax.grid()
    
plt.figure(figsize=(10, 6), dpi=200)
fig, axs = plt.subplots(1, 2, figsize=(20, 12), dpi=200)

plot_check_mates(axs[0], ppochecks, episodes, COUNT)
plot_check_mates(axs[1], a2cchecks, episodes, COUNT)
plt.savefig("results/check_mates.jpeg")
