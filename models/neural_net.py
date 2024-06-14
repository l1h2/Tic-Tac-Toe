import torch
import torch.nn as nn
import torch.nn.functional as F


class TicTacToeNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(9, 100)
        self.fc2 = nn.Linear(100, 100)
        self.fc3 = nn.Linear(100, 9)  # Output layer

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.fc3(x), dim=1)
        return x

    def select_move(self, x: torch.Tensor) -> tuple[int, int]:
        x = self(x)
        flat_move = torch.argmax(x).item()
        return flat_move // 3, flat_move % 3
