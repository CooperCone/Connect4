from doctest import DocTestRunner
from board import Board, Width, Height
from strategy import RandomStrategy
from game import Game
from view import NoView

import random

casesToGenerate = 50
turnDistribution = (1, 10)

i = 0
while i < casesToGenerate:
    numTurns = random.randrange(turnDistribution[0], turnDistribution[1])

    game = Game(RandomStrategy(), RandomStrategy(), NoView())
    game.play(maxTurns=numTurns)

    if game.board.detectWin() == None:
        print(game.board.serialize())
        i += 1
