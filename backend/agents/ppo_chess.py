import torch
from agents import SingleAgentChess
from learnings.ppo import PPO
from chess import info_keys as InfoKeys

from buffer.episode import Episode


class PPOChess(SingleAgentChess):
    def __init__(self, env, learner, episodes, train_on, result_folder, white_ppo_path, black_ppo_path):
        super().__init__(env, learner, episodes, train_on, result_folder)
        self.white_learner = learner
        self.black_learner = learner

        # Load the trained api
        self.white_learner.load_state_dict(torch.load(white_ppo_path))
        self.black_learner.load_state_dict(torch.load(black_ppo_path))

        # Set the api to evaluation mode
        self.white_learner.eval()
        self.black_learner.eval()

    def take_action(self, turn: int, episode: Episode):
        mask = self.env.get_all_actions(turn)[-1]
        state = self.env.get_state(turn)

        # Use the appropriate learner based on the current turn
        if turn == 0:
            action, prob, value = self.white_learner.take_action(state, mask)
        else:
            action, prob, value = self.black_learner.take_action(state, mask)

        rewards, done, infos = self.env.step(action)
        self.moves[turn, self.current_ep] += 1

        self.update_stats(infos)
        goal = InfoKeys.CHECK_MATE_WIN in infos[turn]
        episode.add(state, rewards[turn], action, goal, prob, value, mask)

        # original return statement
        # return done, [state, rewards, action, goal, prob, value, mask]
        return done, [state, rewards, action, goal, prob, value, mask, infos]