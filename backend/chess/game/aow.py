from typing import Union, Optional, List

import gym
from gym.core import RenderFrame

import chess.constants.rewards as Rewards
from chess.game.aow_logic import AoWLogic
from chess.models.board import AoWBoard
from chess.models.cards import DutchWaterline
from chess.models.pieces import King
from chess.models.types import Cell
from chess.utils.pygame import PyGameUtils


class ArtOfWar(gym.Env):
    def __init__(self, max_steps: int = 128, window_size: int = 800, render_mode: str = 'human'):
        self.aow_board = AoWBoard()
        self.pygame_utils = PyGameUtils(window_size=window_size, render_mode=render_mode)
        self.aow_logic = AoWLogic(max_steps=max_steps, board=self.aow_board)

    def step(self, action: int) -> tuple[list[int], bool, list[set]]:
        """
        Take a step in the environment
        :param action: int: The action to take
        :return: tuple[list[int], bool, list[set]]: The rewards, if the game is done, and the info
        """
        assert not self.aow_logic.is_game_done(), "the game is finished reset"
        assert action < self.aow_logic.action_space_length, f"action number must be less than {self.aow_logic.action_space_length}."

        source_pos, possibles, actions_mask = self.aow_logic.get_all_actions(self.aow_logic.turn)
        assert actions_mask[action], f"Cannot Take This Action = {action}, {source_pos[action]} -> {possibles[action]}"

        from_pos = Cell(int(source_pos[action][0]), int(source_pos[action][1]))
        next_pos = Cell(int(possibles[action][0]), int(possibles[action][1]))

        if (self.aow_board.is_piece(self.aow_logic.turn, next_pos, King()) or
                self.aow_board.is_piece(1 - self.aow_logic.turn, Cell(7 - next_pos.row, next_pos.col), King())):
            print(f"King not removed at {7 - next_pos.row}, {next_pos.col}"
                  f" or {from_pos.row}, {from_pos.col},"
                  f" turn: {self.aow_logic.turn}")

        if from_pos == next_pos and self.aow_board.get_piece(from_pos, self.aow_logic.turn).is_upgradable():
            source_pos_piece = self.aow_board.get_piece(Cell(from_pos[0], from_pos[1]), self.aow_logic.turn)
            rewards, infos = self.aow_logic.upgrade_piece(from_pos, self.aow_logic.turn, source_pos_piece)
            end_turn = False
        elif ((from_pos == (2, 0) or from_pos == (3, 0) or from_pos == (4, 0) or from_pos == (5, 0))
              and next_pos == Cell(0, 7)):
            # Get Dutch waterline card from array
            card: DutchWaterline | None = self.aow_board.get_card(turn=self.aow_logic.turn, card=DutchWaterline())
            assert card is not None, "Dutch Waterline card not found"
            card.play(from_pos, self.aow_board, self.aow_logic.turn)

            rewards = self.aow_logic.add_reward(reward=Rewards.DUTCH_WATERLINE, turn=self.aow_logic.turn)
            infos = [set(), set()]
            end_turn = False
        else:
            rewards, infos = self.aow_logic.move_piece(
                from_pos, next_pos, self.aow_logic.turn
            )
            end_turn = True

        rewards, infos = self.aow_logic.update_checks(rewards, infos)
        rewards, infos = self.aow_logic.update_check_mates(rewards, infos)
        rewards, infos = self.aow_logic.update_draw(rewards, infos)

        if from_pos != next_pos or end_turn:
            self.aow_board.add_resources(self.aow_logic.turn, 1)
            self.aow_logic.turn = 1 - self.aow_logic.turn
        self.aow_logic.steps += 1
        return rewards, self.aow_logic.is_game_done(), infos

    def render(self) -> Optional[Union[RenderFrame, List[RenderFrame]]]:
        """
        Render the environment
        :return: Optional[Union[RenderFrame, List[RenderFrame]]]: The rendered frame
        """
        return self.pygame_utils.render(self.aow_board.get_numeric_board())

    def reset(self, **kwargs) -> None:
        """
        Reset the environment
        :param kwargs: dict: The arguments to reset the environment
        """
        self.aow_logic.done = False
        self.aow_logic.turn = 0  # 0 or 1, 0 means white, 1 means black
        self.aow_logic.steps = 0
        self.aow_logic.checked = [False, False]
        self.aow_board.reset()
