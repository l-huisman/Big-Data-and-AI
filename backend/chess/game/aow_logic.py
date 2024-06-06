import numpy as np
from gym import spaces

import chess.constants.info_keys as InfoKeys
import chess.constants.rewards as Rewards
import chess.models.pieces as pieces_module
import chess.pieces as Pieces
from chess.models.board import AoWBoard
from chess.models.cards import DutchWaterline, WarElephantUpgradeCard, WingedKnightUpgradeCard, \
    HopliteUpgradeCard
from chess.models.pieces import *
from chess.models.types import Cell
from chess.utils.cell import CellUtils
from chess.game.check import Check


class AoWLogic:
    def __init__(self, max_steps: int, board: AoWBoard):
        self.action_space_length = 1200  # 3584
        self.action_space = spaces.Discrete(self.action_space_length)  # standard chess board has 1000 possible moves.
        self.observation_space = spaces.Box(0, 7, (128,), dtype=np.int32)

        self.turn: int = Pieces.WHITE
        self.done: bool = False
        self.steps: int = 0
        self.checked: list[bool] = [False, False]
        self.max_steps: int = max_steps
        self.aow_board = board

    def get_source_pos(self, name: str, turn: int) -> np.ndarray:
        cat = name.split("_")[0]
        pos = self.aow_board.pieces[turn][name]
        if pos is None:
            pos = (0, 0)
        _class = getattr(pieces_module, cat.capitalize())
        size = _class().get_possibles_size()
        return np.array([pos] * size)

    def get_actions_for(self, name: str, turn: int, deny_enemy_king: bool = False) -> tuple:
        assert name in self.aow_board.get_pieces_names()[
            turn], f"{name} not in {self.aow_board.get_pieces_names()[turn]}"

        piece_cat = name.split("_")[0]
        piece_pos = self.aow_board.pieces[turn][name]
        src_poses = self.get_source_pos(name, turn)
        piece_class = getattr(pieces_module, piece_cat.capitalize())

        return src_poses, *piece_class().get_actions(self.aow_board, piece_pos, turn, deny_enemy_king)

    def get_all_actions(self, turn: int, deny_enemy_king: bool = False):
        all_possibles = []
        all_source_pos = []
        all_actions_mask = []
        length = 0
        for name in self.aow_board.pieces[turn].keys():
            # DENY ENEMY KING == FOR CHECKMATE VALIDATION ONLY SO ....
            if name == "king_1" and deny_enemy_king:
                continue

            source_pos, possibles, actions_mask = self.get_actions_for(
                name, turn, deny_enemy_king
            )

            all_source_pos.append(source_pos)
            all_possibles.append(possibles)
            all_actions_mask.append(actions_mask)
            length += len(actions_mask)

        for i in range(3):
            source_pos, possibles, actions_mask = self.get_card_upgrade_actions(turn, i)

            all_source_pos.append(source_pos)
            all_possibles.append(possibles)
            all_actions_mask.append(actions_mask)
            length += len(actions_mask)

        possibles, source_pos, actions_mask = (self.aow_board.get_card(
            turn,
            DutchWaterline()).get_actions(
            Cell(0, 0), self.aow_board, turn
        )
        )

        all_possibles.append(possibles)
        all_actions_mask.append(actions_mask)
        all_source_pos.append(source_pos)
        length += len(actions_mask)

        all_actions_mask.append(np.zeros(self.action_space_length - length, dtype=bool))
        return (
            np.concatenate(all_source_pos),
            np.concatenate(all_possibles),
            np.concatenate(all_actions_mask),
        )

    def get_card_upgrade_actions(self, turn: int, card_id: int):
        match card_id:
            case 0:
                return HopliteUpgradeCard().get_actions(self.aow_board, None, turn)
            case 1:
                return WingedKnightUpgradeCard().get_actions(self.aow_board, None, turn)
            case 2:
                return WarElephantUpgradeCard().get_actions(self.aow_board, None, turn)
            case _:
                assert False, f"Invalid card id {card_id}"

    def update_checks(self, rewards: list[int] = None, infos: list[set] = None):
        check = Check(self.aow_board)
        rewards = [0, 0] if rewards is None else rewards
        infos = [set(), set()] if infos is None else infos

        for turn in range(2):
            king_pos = self.aow_board.get_king_position(turn)
            is_check = check.is_check(king_pos, turn)
            self.checked[turn] = is_check
            if is_check:
                rewards[turn] += Rewards.CHECK_LOSE
                rewards[1 - turn] += Rewards.CHECK_WIN

                infos[turn].add(InfoKeys.CHECK_LOSE)
                infos[1 - turn].add(InfoKeys.CHECK_WIN)
                break
        return rewards, infos

    def update_check_mates(self, rewards: list[int] = None, infos: list[set] = None):
        rewards = [0, 0] if rewards is None else rewards
        infos = [set(), set()] if infos is None else infos

        for turn in range(2):
            _, _, actions = self.get_all_actions(turn)
            if np.sum(actions) == 0:
                self.done = True
                rewards[turn] += Rewards.CHECK_MATE_LOSE
                rewards[1 - turn] += Rewards.CHECK_MATE_WIN

                infos[turn].add(InfoKeys.CHECK_MATE_LOSE)
                infos[1 - turn].add(InfoKeys.CHECK_MATE_WIN)
                break

        return rewards, infos

    def update_draw(self, rewards: list[int] = None, infos: list[set] = None):
        rewards = [0, 0] if rewards is None else rewards
        infos = [set(), set()] if infos is None else infos

        if self.steps >= self.max_steps:
            rewards[0] += Rewards.DRAW
            rewards[1] += Rewards.DRAW

            infos[0].add(InfoKeys.DRAW)
            infos[1].add(InfoKeys.DRAW)

        return rewards, infos

    def move_piece(self, src: Cell, dst: Cell, turn: int):
        src = CellUtils.make_cell(src)
        dst = CellUtils.make_cell(dst)
        selected_piece = self.aow_board.get_piece(src, turn)
        selected_piece.set_has_moved()

        if self.aow_board.is_piece(1 - turn, Cell(7 - dst.row, dst.col), King()):
            return [-100, -100], [set(), set()]

        # move piece
        self.aow_board.set_piece(turn, src, Empty())
        self.aow_board.set_piece(turn, dst, selected_piece)

        # remove enemy piece in position
        self.aow_board.set_piece(1 - turn, Cell(7 - dst.row, dst.col), Empty())

        # Set default rewards, [-1, -2], -1 for the player who moved the piece, -2 for the other player
        rewards = [Rewards.MOVE, Rewards.MOVE]
        rewards[1 - turn] *= 0

        self.capture_pawn_by_warelephant(dst.row, dst.col, src.row, src.col, turn)
        self.promote_pawn_or_hoplite(dst, turn)
        # self.castle(src, dst, turn)

        for (key, value) in self.aow_board.pieces[turn].items():
            if value == tuple(src):
                # # Update the location of the piece in the pieces array
                self.aow_board.pieces[turn][key] = (dst.row, dst.col)

        for (key, value) in self.aow_board.pieces[1 - turn].items():
            if value == (7 - dst[0], dst[1]):
                # Remove the location from the piece that was removed in the pieces array
                self.aow_board.pieces[1 - turn][key] = None

                # add a reward for capturing a piece
                selected_piece = key.split("_")[0]
                selected_piece = selected_piece.upper()

                # get the reward from the rewards.py based on the name of the piece
                reward = getattr(Rewards, selected_piece)
                rewards = self.add_reward(rewards, reward, turn)

        return rewards, [set(), set()]

    @staticmethod
    def add_reward(rewards: list[int] = None, reward: int = 0, turn: int = 1) -> list:
        rewards = [Rewards.MOVE, Rewards.MOVE] if rewards is None else rewards
        rewards[turn] += reward
        rewards[1 - turn] += -reward
        return rewards


    def capture_pawn_by_warelephant(self, next_row: int, next_col: int, current_row: int, current_col: int, turn: int):
        if self.aow_board.is_piece(turn, Cell(next_row, next_col), Warelephant()):
            min_row, max_row = min(current_row, next_row), max(current_row, next_row)
            min_col, max_col = min(current_col, next_col), max(current_col, next_col)

            for r in range(min_row + 1, max_row):
                if self.aow_board.is_piece(1 - turn, Cell(7 - r, current_col), Pawn()):
                    self.aow_board.set_piece(1 - turn, Cell(7 - r, current_col), Empty())

            for c in range(min_col + 1, max_col):
                if self.aow_board.is_piece(1 - turn, Cell(7 - current_row, c), Pawn()):
                    self.aow_board.set_piece(1 - turn, Cell(7 - current_row, c), Empty())


    def is_game_done(self):
        return self.done or (self.steps >= self.max_steps)

    def promote_pawn_or_hoplite(self, pos: Cell, turn: int):
        """
        Promote pawn or hoplite to queen if it reaches the last row
        :param pos: Position of the piece
        :param turn: Turn of the player
        """
        if pos.row != 7:
            return

        # Check if the piece is a pawn and if it has reached the last row and upgrade it to a queen
        if self.aow_board.is_piece(turn, pos, Pawn()):
            self.upgrade_piece(pos, turn, self.aow_board.get_piece(pos, turn), Queen())

        # Check if the piece is a hoplite and if it has reached the last row and upgrade it to a queen
        if self.aow_board.is_piece(turn, pos, Hoplite()):
            self.upgrade_piece(pos, turn, self.aow_board.get_piece(pos, turn), Queen())

    def upgrade_piece(self, pos: Cell, turn: int, piece_to_upgrade: Piece, upgrade_to: Piece = None):
        if not piece_to_upgrade.is_upgradable():
            assert False, f"Piece {piece_to_upgrade} is not upgradable"

        rewards = [0, 0]
        rewards[turn] = Rewards.UPGRADE_PIECE
        rewards[1 - turn] = 0

        new_piece = piece_to_upgrade.get_upgrade_options()[0]

        if upgrade_to is not None:
            for option in piece_to_upgrade.get_upgrade_options():
                if option.get_name().lower() == upgrade_to.get_name().lower():
                    new_piece = option
                    print(f"1{new_piece.get_name()}")
                    break

        print(f"1{new_piece.get_name()}")
        # get piece_name from position
        piece_name = None
        for key, value in self.aow_board.pieces[turn].items():
            print(f" In loop:{new_piece.get_name()} pos: {pos.row, pos.col}")
            print(key, value, pos.row, pos.col)
            if value == (pos.row, pos.col):
                piece_name = key
                print(f"Piece name: {piece_name}")
                break

        print(self.aow_board.pieces[turn].items())

        print(f"2{new_piece.get_name()}")
        # get piece at pos
        print(self.aow_board.get_piece(pos, turn).get_name())

        print(isinstance(new_piece, Empty) or piece_name is None)
        print(isinstance(new_piece, Empty))
        print(piece_name is None)

        # return rewards if the piece is empty (This happens because of Dutch waterline,
        # which can be activated on an empty space)
        if isinstance(new_piece, Empty) or piece_name is None:
            return [0, 0], [set(), set()]

        print(f"3{new_piece.get_name()}")

        split_piece_name = piece_name.split("_")

        print(f"4{new_piece.get_name()}")

        if len(split_piece_name) < 2:
            return [0, 0], [set(), set()]

        print(f"5{new_piece.get_name()}")

        new_piece_name = f"{new_piece.get_name().lower()}_{split_piece_name[1]}"
        print(f"Upgrading {piece_name} to {new_piece_name}")

        # update the piece
        self.aow_board.pieces[turn][f"{new_piece.get_name().lower()}_{piece_name.split('_')[1]}"] = \
            self.aow_board.pieces[turn].pop(piece_name)
        new_piece.set_has_moved(True)
        self.aow_board.set_piece(turn, pos, new_piece)
        self.remove_resources(turn, new_piece)
        return rewards, [set(), set()]

    def remove_resources(self, turn: int, selected_piece: Piece):
        match selected_piece.get_piece_number():
            case Pieces.HOPLITE:
                self.aow_board.remove_resources(turn, 2)
            case Pieces.WINGED_KNIGHT:
                self.aow_board.remove_resources(turn, 3)
            case Pieces.WARELEPHANT:
                self.aow_board.remove_resources(turn, 5)

    def castle(self, current_pos: Cell, next_pos: Cell, turn: int):
        current_pos = CellUtils.make_cell(current_pos)
        next_pos = CellUtils.make_cell(next_pos)

        if self.aow_board.is_piece(turn, next_pos, King()):
            if current_pos.col - next_pos.col == 2:
                self.aow_board.set_piece(turn, Cell(current_pos.row, 3),
                                         self.aow_board.get_piece(Cell(current_pos.row, 0), turn))
                self.aow_board.set_piece(turn, Cell(current_pos.row, 0), Empty())
            elif current_pos.col - next_pos.col == -2:
                self.aow_board.set_piece(turn, Cell(current_pos.row, 5),
                                         self.aow_board.get_piece(Cell(current_pos.row, 7), turn))
                self.aow_board.set_piece(turn, Cell(current_pos.row, 7), Empty())
