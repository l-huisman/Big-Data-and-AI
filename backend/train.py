import os
import sys

from dotenv import load_dotenv

from agents import DoubleAgents
from aow.game.aow import ArtOfWar
from learnings.a2c import A2C
from learnings.dqn import DQNLearner
from learnings.ppo import PPO

load_dotenv()

if __name__ == "__main__":
    aow = ArtOfWar(
        window_size=int(os.getenv("AOW_WINDOW_SIZE")),
        max_steps=int(os.getenv("AOW_MAX_STEPS")),
        render_mode=os.getenv("AOW_RENDER_MODE"),
    )
    aow.reset()

    possible_models = ["dqn", "ppo", "a2c"]
    sys_args = sys.argv
    if len(sys_args) <= 1 or sys_args[1] not in possible_models:
        print("Please provide a model (dqn, ppo or a2c) to train.")
        sys.exit()

    agent = None
    if sys_args[1] == "ppo":
        ppo = PPO(
            aow,
            hidden_layers=(int(os.getenv("PPO_HIDDEN_LAYERS_SIZE")),) * int(os.getenv("PPO_HIDDEN_LAYERS_COUNT")),
            epochs=int(os.getenv("PPO_EPOCHS")),
            buffer_size=int(os.getenv("BUFFER_SIZE")) * 2,
            batch_size=int(os.getenv("BATCH_SIZE")),
            gamma=float(os.getenv("PPO_GAMMA")),
            gae_lambda=float(os.getenv("PPO_GAE_LAMBDA")),
            policy_clip=float(os.getenv("PPO_POLICY_CLIP")),
            learning_rate=float(os.getenv("PPO_LEARNING_RATE")),
        )

        print(ppo.device)
        print(ppo)

        agent = DoubleAgents(
            env=aow,
            learner=ppo,
            episodes=int(os.getenv("EPISODES")),
            train_on=int(os.getenv("BUFFER_SIZE")),
            result_folder=os.getenv("PPO_RESULT_FOLDER"),
        )
    elif sys_args[1] == "dqn":
        dqn = DQNLearner(
            environment=aow,
            epochs=int(os.getenv("DQN_EPOCHS")),
            gamma=float(os.getenv("DQN_GAMMA")),
            learning_rate=float(os.getenv("DQN_LEARNING_RATE")),
            hidden_layers=(int(os.getenv("DQN_HIDDEN_LAYERS_SIZE")),) * int(os.getenv("DQN_HIDDEN_LAYERS_COUNT")),
            buffer_size=int(os.getenv("BUFFER_SIZE")),
            batch_size=int(os.getenv("BATCH_SIZE")),
            epsilon=float(os.getenv("DQN_EPSILON")),
            epsilon_decay=float(os.getenv("DQN_EPSILON_DECAY")),
            epsilon_min=float(os.getenv("DQN_EPSILON_MIN")),
            tau=float(os.getenv("DQN_TAU")),
            update_every=int(os.getenv("DQN_UPDATE_EVERY")),
        )
        print(dqn.device)
        print(dqn)

        agent = DoubleAgents(
            env=aow,
            learner=dqn,
            episodes=int(os.getenv("EPISODES")),
            train_on=int(os.getenv("BUFFER_SIZE")),
            result_folder=os.getenv("DQN_RESULT_FOLDER"),
        )

    elif sys_args[1] == "a2c":
        a2c = A2C(
            environment=aow,
            epochs=int(os.getenv("A2C_EPOCHS")),
            hidden_layers=(int(os.getenv("A2C_HIDDEN_LAYERS_SIZE")),) * int(os.getenv("A2C_HIDDEN_LAYERS_COUNT")),
            buffer_size=int(os.getenv("BUFFER_SIZE")),
            batch_size=int(os.getenv("BATCH_SIZE")),
            gamma=float(os.getenv("A2C_GAMMA")),
            gae_lambda=float(os.getenv("A2C_GAE_LAMBDA")),
            learning_rate=float(os.getenv("A2C_LEARNING_RATE"))
        )

        print(a2c.device)
        print(a2c)

        agent = DoubleAgents(
            env=aow,
            learner=a2c,
            episodes=int(os.getenv("EPISODES")),
            train_on=int(os.getenv("BUFFER_SIZE")),
            result_folder=os.getenv("A2C_RESULT_FOLDER"),
        )

    agent.train(render_each=int(os.getenv("RENDER_EACH")), save_on_learn=bool(os.getenv("SAVE_ON_LEARN")))
    agent.save()
    aow.close()
