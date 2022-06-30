from enum import Enum

class Player(Enum):
    Red = 1
    Blue = 2

    def __str__(self):
        return self.name

def getOpposingPlayer(player: Player):
    if player == Player.Red:
        return Player.Blue
    elif player == Player.Blue:
        return Player.Red
    else:
        assert(False)
