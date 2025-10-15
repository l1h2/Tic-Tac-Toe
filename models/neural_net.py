import torch
import torch.nn as nn
from torch.optim.adam import Adam
from torch.utils.data import DataLoader


class TicTacToeNet(nn.Module):
    """
    ### Neural network for playing Tic-Tac-Toe.

    The neural network has 2 layers with ReLU activation functions with 128 neurons each.
    The output layer uses the softmax activation function.

    #### Attributes:
    - `relu (nn.ReLU)`: The ReLU activation function.
    - `softmax (nn.Softmax)`: The softmax activation function.
    - `fc1 (nn.Linear)`: The first fully connected layer.
    - `fc2 (nn.Linear)`: The second fully connected layer.
    - `output (nn.Linear)`: The output layer.
    - `state_loaded (bool)`: Whether the model state has been loaded.

    #### Methods:
    - `forward(x: torch.Tensor) -> torch.Tensor`: The forward pass of the neural network.
    - `select_move(x: torch.Tensor) -> tuple[int, int]`: Selects the move with the highest probability.
    - `get_move_probabilities(x: torch.Tensor) -> list[float]`: Gets the probabilities of each move.
    - `train_model(train_loader: DataLoader[torch.Tuple[torch.Tensor]], num_epochs: int = 1000) -> dict[str, torch.Tensor]`: Trains the model on a game states dataset.
    - `test_model(test_loader: DataLoader[torch.Tuple[torch.Tensor]], model_file: str = None) -> list[int]`: Tests the model on a game states dataset.
    """

    def __init__(self, state_file: str | None = None):
        super().__init__()
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)
        self.fc1 = nn.Linear(9, 128)
        self.fc2 = nn.Linear(128, 128)
        self.output = nn.Linear(128, 9)
        self.state_loaded = False

        if state_file:
            self.load_state_dict(torch.load(state_file))
            self.state_loaded = True

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the neural network.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The output tensor.
        """
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.output(x)
        return x if self.training else self.softmax(x)

    def select_move(self, x: torch.Tensor) -> tuple[int, int]:
        """
        Selects the move with the highest probability.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            tuple[int, int]: The selected move.
        """
        self.eval()
        x = self(x)
        flat_move = torch.argmax(x).item()
        return int(flat_move // 3), int(flat_move % 3)

    def get_move_probabilities(self, x: torch.Tensor) -> list[float]:
        """
        Gets the probabilities of each move.

        Args:
            x (torch.Tensor): The input tensor.

        Returns:
            list: The probabilities of each move.
        """
        self.eval()
        x = self(x)
        return x[0].tolist()  # type: ignore

    def train_model(
        self,
        train_loader: DataLoader[tuple[torch.Tensor, ...]],
        num_epochs: int = 1000,
    ) -> dict[str, torch.Tensor]:
        """
        Trains the model on a game states dataset.

        Args:
            train_loader (DataLoader): The DataLoader for the training data.
            num_epochs (int): The number of epochs to train the model.

        Returns:
            dict: The state dictionary of the trained model.
        """
        self.state_loaded = False
        loss_fn = nn.CrossEntropyLoss()
        optimizer = Adam(self.parameters(), lr=0.01)

        best_loss = float("inf")
        patience = 10
        patience_counter = 0
        min_delta = 1e-6
        avg_loss = 0
        last_epoch = 0

        for epoch in range(num_epochs):
            last_epoch = epoch
            self.train()
            batch_loss = 0
            batch_count = 0

            for states_batch, targets_batch in train_loader:
                optimizer.zero_grad()
                outputs = self(states_batch)
                loss = loss_fn(outputs, targets_batch)
                loss.backward()
                optimizer.step()

                batch_loss += loss.item()
                batch_count += 1

            avg_loss = batch_loss / batch_count

            if epoch % 10 == 0:
                print(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss}")

            if best_loss - min_delta < avg_loss < best_loss:
                patience_counter += 1
            else:
                patience_counter = 0
                best_loss = min(best_loss, avg_loss)

            if patience_counter > patience:
                print(f"Early stopping at epoch {epoch+1}")
                break

        self.state_loaded = True
        print(f"Training complete: Epochs: {last_epoch+1}, Loss: {avg_loss}")
        return self.state_dict()

    def test_model(
        self,
        test_loader: DataLoader[tuple[torch.Tensor, ...]],
        model_file: str | None = None,
    ) -> list[int]:
        """
        Tests the model on a game states dataset.

        Args:
            datafile (str): The path to the data file.
            model_file (str): The model file to be loaded.

        Returns:
            list[int]: The predictions of the model.
        """
        if not self.state_loaded and model_file:
            self.load_state_dict(torch.load(model_file))
            self.state_loaded = True

        self.eval()
        correct = 0
        total = 0
        predictions: list[int] = []

        with torch.no_grad():
            for states, targets in test_loader:
                outputs = self(states)
                _, predicted = torch.max(outputs, 1)
                total += targets.size(0)
                correct += (predicted == targets).sum().item()
                predictions.extend(predicted.tolist())  # type: ignore

        print(f"Accuracy: {100 * correct / total:.2f}%")
        return predictions
