import sys

from agents import DoubleAgentsChess
from chess import Chess
from learnings.dqn import DQNLearner
from learnings.ppo import PPO
from learnings.a2c import A2C

args = dict({
    "episodes": 100,
    "render_each": 20,
    "save_on_learn": True,
    "chess": dict({
        "window_size": 512,
        "max_steps": 128,
        "render_mode": "rgb_array",
    }),
    "ppo": dict({
        "hidden_layers": (2048,) * 4,
        "epochs": 100,
        "buffer_size": 32,
        "batch_size": 128,
        "result_folder": "results/DoubleAgentsPPO",
    }),
    "a2c": dict({
        "hidden_layers": (2048,) * 4,
        "epochs": 100,
        "buffer_size": 32,
        "batch_size": 128,
        "result_folder": "results/DoubleAgentsA2C",
    }),
    "dqn": dict({
        "epochs": 100,
        "gamma": 0.99,
        "learning_rate": 0.003,
        "hidden_layers": (2048,) * 4,
        "buffer_size": 32,
        "batch_size": 128,
        "epsilon": 0.1,
        "epsilon_decay": 0.995,
        "epsilon_min": 0.01,
        "tau": 0.99,
        "update_every": 4,
        "result_folder": "results/DoubleAgentsDQN",
    }),
})

if __name__ == "__main__":
    chess = Chess(
        window_size=args["chess"]["window_size"],
        max_steps=args["chess"]["max_steps"],
        render_mode=args["chess"]["render_mode"]
    )
    chess.reset()

    possible_models = ["dqn", "ppo", "a2c"]
    sys_args = sys.argv
    if len(sys_args) <= 1 or sys_args[1] not in possible_models:
        print("Please provide a model (dqn, ppo or a2c) to train.")
        sys.exit()

    agent = None
    if sys_args[1] == "ppo":
        ppo = PPO(
            chess,
            hidden_layers=args["ppo"]["hidden_layers"],
            epochs=args["ppo"]["epochs"],
            buffer_size=args["ppo"]["buffer_size"] * 2,
            batch_size=args["ppo"]["batch_size"],
        )

        print(ppo.device)
        print(ppo)

        agent = DoubleAgentsChess(
            env=chess,
            learner=ppo,
            episodes=args["episodes"],
            train_on=args["ppo"]["buffer_size"],
            result_folder=args["ppo"]["result_folder"],
        )

    elif sys_args[1] == "dqn":
        dqn = DQNLearner(
            environment=chess,
            epochs=args["dqn"]["epochs"],
            gamma=args["dqn"]["gamma"],
            learning_rate=args["dqn"]["learning_rate"],
            hidden_layers=args["dqn"]["hidden_layers"],
            buffer_size=args["dqn"]["buffer_size"],
            batch_size=args["dqn"]["batch_size"],
            epsilon=args["dqn"]["epsilon"],
            epsilon_decay=args["dqn"]["epsilon_decay"],
            epsilon_min=args["dqn"]["epsilon_min"],
            tau=args["dqn"]["tau"],
            update_every=args["dqn"]["update_every"],
        )
        print(dqn.device)
        print(dqn)

        agent = DoubleAgentsChess(
            env=chess,
            learner=dqn,
            episodes=args["episodes"],
            train_on=args["dqn"]["buffer_size"],
            result_folder=args["dqn"]["result_folder"],
        )

    elif sys_args[1] == "a2c":
        a2c = A2C(
            environment=chess,
            epochs=args["a2c"]["epochs"],
            hidden_layers=args["a2c"]["hidden_layers"],
            buffer_size=args["a2c"]["buffer_size"],
            batch_size=args["a2c"]["batch_size"],
        )
        print(a2c.device)
        print(a2c)

        agent = DoubleAgentsChess(
            env=chess,
            learner=a2c,
            episodes=args["episodes"],
            train_on=args["a2c"]["buffer_size"],
            result_folder=args["a2c"]["result_folder"],
        )

    agent.train(render_each=args["render_each"], save_on_learn=args["save_on_learn"])
    agent.save()
    chess.close()
