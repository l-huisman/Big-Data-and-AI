from chess.models.pieces import Piece


class AoWLogic:
    def get_source_pos(self, name: str, turn: int):
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

        possibles, source_pos, actions_mask = self.aow_board.get_card(turn, DutchWaterline()).get_actions(Cell(0, 0),
                                                                                                          self.aow_board,
                                                                                                          turn)
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

    def is_neighbor_enemy_king(self, pos: Cell, turn: int) -> bool:
        row, col = pos
        row_enemy_king, col_enemy_king = self.aow_board.get_king_position(1 - turn)
        row_enemy_king = 7 - row_enemy_king
        diff_row = abs(row - row_enemy_king)
        diff_col = abs(col - col_enemy_king)
        return diff_row <= 1 and diff_col <= 1

    def is_check(self, king_pos: Cell, turn: int) -> bool:
        rk, ck = king_pos

        diagonal_pieces = (Bishop, Queen)
        straight_pieces = (Rook, Queen, Warelephant)

        # GO TO UP ROW
        for r in range(rk + 1, 8):
            if not self.aow_board.is_empty(Cell(r, ck), turn):
                break
            p = self.aow_board.get_piece(Cell(7 - r, ck), 1 - turn)
            if isinstance(p, straight_pieces):
                return True

        # GO TO DOWN ROW
        for r in range(rk - 1, -1, -1):
            if not self.aow_board.is_empty(Cell(r, ck), turn):
                break
            p = self.aow_board.get_piece(Cell(7 - r, ck), 1 - turn)
            if isinstance(p, straight_pieces):
                return True

        # GO TO RIGHT COL
        for c in range(ck + 1, 8):
            if not self.aow_board.is_empty(Cell(rk, c), turn):
                break
            p = self.aow_board.get_piece(Cell(7 - rk, c), 1 - turn)
            if isinstance(p, straight_pieces):
                return True

        # GOT TO LEFT COL
        for c in range(ck - 1, -1, -1):
            if not self.aow_board.is_empty(Cell(rk, c), turn):
                break
            p = self.aow_board.get_piece(Cell(7 - rk, c), 1 - turn)
            if isinstance(p, straight_pieces):
                return True

        # CROSS DOWN
        for r in range(rk + 1, 8):
            # RIGHT
            d = r - rk
            for c in [ck + d, ck - d]:
                if not self.aow_board.is_in_range(Cell(r, c)):
                    continue

                if not self.aow_board.is_empty(Cell(r, c), turn):
                    break

                p = self.aow_board.get_piece(Cell(7 - r, c), 1 - turn)

                if isinstance(p, diagonal_pieces):
                    return True

                if d == 1 and (isinstance(p, Pawn) or isinstance(p, Hoplite)):
                    return True

        # CROSS UP
        for r in range(rk - 1, -1, -1):
            d = r - rk
            for c in [ck + d, ck - d]:
                if not self.aow_board.is_in_range(Cell(r, c)):
                    continue

                if not self.aow_board.is_empty(Cell(r, c), turn):
                    break

                p = self.aow_board.get_piece(Cell(7 - r, c), 1 - turn)
                if p in diagonal_pieces:
                    return True

                if d == 1 and (isinstance(p, Pawn) or isinstance(p, Hoplite)):
                    return True

        # KNIGHTS
        for r, c in Knight().get_moves():
            nr, nc = rk + r, ck + c
            if not self.aow_board.is_in_range(Cell(nr, nc)):
                continue
            if self.aow_board.is_piece(1 - turn, Cell(7 - nr, nc), Knight()):
                return True

        # WINGED KNIGHTS
        for r, c in Wingedknight().get_moves():
            nr, nc = rk + r, ck + c
            if not self.aow_board.is_in_range(Cell(nr, nc)):
                continue
            if self.aow_board.is_piece(1 - turn, Cell(7 - nr, nc), Wingedknight()):
                return True
        return False

    def update_checks(self, rewards: list[int] = None, infos: list[set] = None):
        rewards = [0, 0] if rewards is None else rewards
        infos = [set(), set()] if infos is None else infos

        for turn in range(2):
            king_pos = self.aow_board.get_king_position(turn)
            is_check = self.is_check(king_pos, turn)
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
        piece = self.aow_board.get_piece(src, turn)
        piece.set_has_moved()

        if self.aow_board.is_piece(1 - turn, Cell(7 - dst.row, dst.col), King()):
            return [0, 0], [set(), set()]

        # move piece
        self.aow_board.set_piece(turn, src, Empty())
        self.aow_board.set_piece(turn, dst, piece)

        # remove enemy piece in position
        self.aow_board.set_piece(1 - turn, Cell(7 - dst.row, dst.col), Empty())

        # Set default rewards, [-1, -2], -1 for the player who moved the piece, -2 for the other player
        rewards = [Rewards.MOVE, Rewards.MOVE]
        rewards[1 - turn] *= 0

        self.capture_pawn_by_warelephant(dst.row, dst.col, src.row, src.col, turn)
        self.promote_pawn_or_hoplite(dst, turn)

        for (key, value) in self.aow_board.pieces[turn].items():
            if value == tuple(src):
                # # Update the location of the piece in the pieces array
                self.aow_board.pieces[turn][key] = (dst.row, dst.col)

        for (key, value) in self.aow_board.pieces[1 - turn].items():
            if value == (7 - dst[0], dst[1]):
                # Remove the location from the piece that was removed in the pieces array
                self.aow_board.pieces[1 - turn][key] = None

                # add a reward for capturing a piece
                piece = key.split("_")[0]
                piece = piece.upper()

                # get the reward from the rewards.py based on the name of the piece
                reward = getattr(Rewards, piece)
                rewards = self.add_reward(rewards, reward, turn)

        return rewards, [set(), set()]

    @staticmethod
    def add_reward(rewards: list[int] = None, reward: int = 0, turn: int = 1) -> list:
        rewards = [Rewards.MOVE, Rewards.MOVE] if rewards is None else rewards
        rewards[turn] += reward
        rewards[1 - turn] += -reward
        return rewards

    def capture_pawn_by_warelephant(self, next_row: int, next_col: int, current_row: int, current_col: int, turn: int):
        if self.aow_board.is_piece(turn, Cell(current_row, current_col), Warelephant()):
            if current_row == next_row:
                start_col = min(current_col, next_col) + 1
                end_col = max(current_col, next_col)
                for col in range(start_col, end_col):
                    if self.aow_board.is_piece(pos=Cell(current_row, col), turn=turn,
                                               piece=Pawn()) or self.aow_board.is_piece(pos=Cell(7 - current_row, col),
                                                                                        turn=1 - turn, piece=Hoplite()):
                        self.aow_board.set_piece(turn, Cell(current_row, col), Empty())
                        self.aow_board.set_piece(1 - turn, Cell(7 - current_row, col), Empty())
                        for key, value in self.aow_board.pieces[turn].items():
                            if value == (current_row, col):
                                self.aow_board.pieces[turn][key] = None
                        for key, value in self.aow_board.pieces[1 - turn].items():
                            if value == (7 - current_row, col):
                                self.aow_board.pieces[1 - turn][key] = None

            elif current_col == next_col:
                start_row = min(current_row, next_row) + 1
                end_row = max(current_row, next_row)
                for row in range(start_row, end_row):
                    if (self.aow_board.is_piece(pos=Cell(row, current_col), turn=turn, piece=Pawn()) or
                            self.aow_board.is_piece(pos=Cell(row, current_col), turn=turn, piece=Hoplite()) or
                            self.aow_board.is_piece(pos=Cell(7 - row, current_col), turn=1 - turn, piece=Pawn()) or
                            self.aow_board.is_piece(pos=Cell(7 - row, current_col), turn=1 - turn, piece=Hoplite())):
                        self.aow_board.set_piece(turn, Cell(row, current_col), Empty())
                        self.aow_board.set_piece(1 - turn, Cell(7 - row, current_col), Empty())
                    for key, value in self.aow_board.pieces[turn].items():
                        if value == (row, current_col):
                            self.aow_board.pieces[turn][key] = None
                    for key, value in self.aow_board.pieces[1 - turn].items():
                        if value == (7 - row, current_col): \
                                self.aow_board.pieces[1 - turn][key] = None

    def is_game_done(self):
        return self.done or (self.steps >= self.max_steps)

    def promote_pawn_or_hoplite(self, pos: Cell, turn: int):
        if (self.aow_board.is_piece(turn, pos, Pawn()) or
            self.aow_board.is_piece(turn, pos, Hoplite())) and pos.row == 7:
            self.aow_board.set_piece(turn, pos, Queen())

    def upgrade_piece(self, pos: Cell, turn: int, piece_to_upgrade: Piece):
        if not piece_to_upgrade.is_upgradable():
            assert False, f"Piece {piece_to_upgrade} is not upgradable"

        rewards = [0, 0]
        rewards[turn] = Rewards.UPGRADE_PIECE
        rewards[1 - turn] = 0
        new_piece = piece_to_upgrade.get_upgrade_options()[0]

        # get piece_name from position
        piece_name = None
        for key, value in self.aow_board.pieces[turn].items():
            if value == (pos.row, pos.col):
                piece_name = key
                break

        # return rewards if the piece is empty (This happens because of dutch waterline,
        # which can be activated on an empty space)
        if isinstance(new_piece, Empty) or piece_name is None:
            return [0, 0], [set(), set()]

        split_piece_name = piece_name.split("_")

        if len(split_piece_name) < 2:
            return [0, 0], [set(), set()]

        # update the piece
        self.aow_board.pieces[turn][f"{new_piece.get_name().lower()}_{piece_name.split('_')[1]}"] = \
            self.aow_board.pieces[
                turn].pop(piece_name)
        new_piece.set_has_moved(True)
        self.aow_board.set_piece(turn, pos, new_piece)
        self.remove_resources(turn, new_piece)
        return rewards, [set(), set()]

    def remove_resources(self, turn: int, piece: Piece):
        match piece.get_piece_number():
            case Pieces.HOPLITE:
                self.aow_board.remove_resources(turn, 2)
            case Pieces.WINGED_KNIGHT:
                self.aow_board.remove_resources(turn, 3)
            case Pieces.WARELEPHANT:
                self.aow_board.remove_resources(turn, 5)