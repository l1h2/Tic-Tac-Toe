from game import Game, Player
from models import Models
from utils import Players, PlayerType

if __name__ == "__main__":
    X = Player(Players.X, PlayerType.HUMAN, Models.HARD)
    O = Player(Players.O, PlayerType.HUMAN, Models.HARD)
    move_hints = True

    game = Game(X, O, move_hints)
    game.run()
