from chess import Chess
from agents import SingleAgentChess, DoubleAgentsChess
from learnings.ppo import PPO
from learnings.dqn import DQNLearner

buffer_size = 32
if __name__ == "__main__":
    chess = Chess(window_size=512, max_steps=128, render_mode="rgb_array")
    chess.reset()

    # ppo = PPO(
    #     chess,
    #     hidden_layers=(2048,) * 4,
    #     epochs=100,
    #     buffer_size=buffer_size * 2,
    #     batch_size=128,
    # )
    #
    # print(ppo.device)
    # print(ppo)

    dqn = DQNLearner(
        environment=chess,
        epochs=100,
        gamma=0.99,
        learning_rate=0.003,
        hidden_layers=(2048,) * 4,
        buffer_size=buffer_size * 2,
        batch_size=128,
        epsilon=0.1,
        epsilon_decay=0.995,
        epsilon_min=0.01,
        tau=0.99,
        update_every=4,
    )
    print(dqn.device)
    print(dqn)
    print("-" * 64)

    agent = DoubleAgentsChess(
        env=chess,
        learner=dqn,
        episodes=100,
        train_on=buffer_size,
        result_folder="results/DoubleAgents",
    )
    agent.train(render_each=20, save_on_learn=True)
    agent.save()
    chess.close()
