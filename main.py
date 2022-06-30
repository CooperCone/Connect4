from game import Game
from strategy import *
from valueHeuristics import *
import logging

logging.basicConfig(filename=f'game.log',
    filemode='w',
    format='%(name)s %(message)s',
    level=logging.DEBUG)

game = Game(ManualStrategy(), MinimaxStrategy(4, runHeuristic, Player.Blue))
game.play()
