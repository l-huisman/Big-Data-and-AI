import torch.nn as nn
from utils import build_base_model


class DQN(nn.Module):
    def __init__(self, state_dim: int, action_dim: int, hidden_layers: tuple[int]):
        super().__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_layers = hidden_layers
        self.model = build_base_model(
            state_dim, hidden_layers, action_dim, nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.model(x)
