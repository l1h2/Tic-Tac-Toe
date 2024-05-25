from config import Players, PlayerType
from game import Game, Player
from models import Models

if __name__ == "__main__":
    X = Player(Players.X, PlayerType.HUMAN)
    O = Player(Players.O, PlayerType.COMPUTER, Models.HARD)
    game = Game(X, O)
    game.run()
