import torch
import torch.nn as nn
import torch.nn.functional as F


class TicTacToeNet(nn.Module):
    """
    ### Neural network for playing Tic-Tac-Toe.

    The neural network has 2 layers with ReLU activation functions with 100 neurons each.
    The output layer uses the softmax activation function.

    #### Attributes:
    - `fc1 (nn.Linear)`: The first fully connected layer.
    - `fc2 (nn.Linear)`: The second fully connected layer.
    - `fc3 (nn.Linear)`: The output layer.

    #### Methods:
    - `forward(x: torch.Tensor) -> torch.Tensor`: The forward pass of the neural network.
    - `select_move(x: torch.Tensor) -> tuple[int, int]`: Selects the move with the highest probability.
    """

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(9, 100)
        self.fc2 = nn.Linear(100, 100)
        self.fc3 = nn.Linear(100, 9)  # Output layer

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the neural network.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The output tensor.
        """
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.fc3(x), dim=1)
        return x

    def select_move(self, x: torch.Tensor) -> tuple[int, int]:
        """
        Selects the move with the highest probability.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            tuple[int, int]: The selected move.
        """
        x = self(x)
        flat_move = torch.argmax(x).item()
        return flat_move // 3, flat_move % 3

    def get_move_probabilities(self, x: torch.Tensor) -> list[float]:
        """
        Gets the probabilities of each move.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            list: The probabilities of each move.
        """
        x = self(x)
        return x[0].tolist()
