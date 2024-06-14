from game import Game, Player
from models import Models
from utils import Players, PlayerType

if __name__ == "__main__":
    X = Player(Players.X, PlayerType.COMPUTER, Models.HARD)
    O = Player(Players.O, PlayerType.HUMAN)
    game = Game(X, O)
    game.run()
