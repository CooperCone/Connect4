from enum import IntEnum

class Player(IntEnum):
    Red = 0
    Blue = 1

    def __str__(self):
        return self.name

def getOpposingPlayer(player: Player):
    if player == Player.Red:
        return Player.Blue
    elif player == Player.Blue:
        return Player.Red
    else:
        assert(False)
