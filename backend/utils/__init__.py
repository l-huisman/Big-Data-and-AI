import re

import cv2
import numpy as np
import torch as T
import torch.nn as nn


def build_base_model(
        input_size: int,
        hidden_layers: tuple[int],
        output_size: int,
        last_activation: nn.Module = nn.Identity(),
) -> nn.Module:
    layers = [
        nn.Linear(input_size, hidden_layers[0]),
        nn.ReLU(),
    ]

    for i in range(len(hidden_layers) - 1):
        in_features = hidden_layers[i]
        out_features = hidden_layers[i + 1]
        layers += [
            nn.Linear(in_features, out_features),
            nn.ReLU(),
        ]

    layers += [nn.Linear(hidden_layers[-1], output_size), last_activation]

    return nn.Sequential(*layers)


def make_batch_ids(n: int, batch_size: int, shuffle: bool = True) -> np.ndarray:
    starts = np.arange(0, n, batch_size)
    indices = np.arange(n, dtype=np.int64)
    if shuffle:
        np.random.shuffle(indices)
    return [indices[i: i + batch_size] for i in starts]


def tensor_to_numpy(x: T.Tensor) -> np.ndarray:
    return x.detach().cpu().numpy()


def save_to_video(path: str, frames: np.ndarray, fps: int = 2):
    size = frames.shape[1:3]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        path,
        fourcc,
        fps,
        size,
    )
    for f in frames:
        out.write(f)
    out.release()


def convert_move_to_positions(action_str):
    from_pos = convert_cell_to_position(action_str[:2])
    to_pos = convert_cell_to_position(action_str[2:])
    return from_pos, to_pos


def convert_cell_to_position(cell):
    f1 = int(cell[1]) - 1
    f2 = ord(cell[0]) - ord('a')
    return np.array([f1, f2])


def matches_regex(action_str, regex):
    return re.match(regex, action_str) is not None


def reverse_move(move):
    return move[0] + "" + str(9 - int(move[1])) + "" + move[2] + "" + str(9 - int(move[3]))
