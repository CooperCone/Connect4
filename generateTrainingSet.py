from doctest import DocTestRunner
from board import Board, Width, Height
from strategy import RandomStrategy
from game import Game
from view import NoView

import random

casesToGenerate = 50
turnDistribution = (1, 10)

for i in range(casesToGenerate):
    board = Board()

    numTurns = random.randrange(turnDistribution[0], turnDistribution[1])

    game = Game(RandomStrategy(), RandomStrategy(), NoView())
    game.play(maxTurns=numTurns)

    print(game.board.serialize())
