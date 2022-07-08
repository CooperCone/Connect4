from doctest import DocTestRunner
from board import Board, Width, Height
from strategy import RandomStrategy
from player import *
from game import Game
from view import NoView
from log import NoLogging

import random
import copy

casesToGenerate = 50
turnDistribution = (1, 10)

i = 0
while i < casesToGenerate:
    numTurns = random.randrange(turnDistribution[0], turnDistribution[1])

    game = Game(RandomStrategy(), RandomStrategy(), NoView(), NoLogging())
    game.play(maxTurns=numTurns)

    # Make sure you can't win in two moves
    if game.board.detectWin() != None:
        continue

    foundWin = False
    firstBoard = copy.deepcopy(game.board)
    for redMove in firstBoard.getValidColumns():
        newBoard = copy.deepcopy(firstBoard)
        newBoard.placePiece(redMove, Player.Red)

        if newBoard.detectWin() != None:
            foundWin = True
            break

        for blueMove in newBoard.getValidColumns():
            secondBoard = copy.deepcopy(newBoard)
            secondBoard.placePiece(blueMove, Player.Blue)

            if secondBoard.detectWin() != None:
                foundWin = True
                break
        
        if foundWin:
            break
    
    if foundWin:
        continue

    print(game.board.serialize())
    i += 1
