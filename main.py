from game import Game
from strategy import *
from valueHeuristics import *
from view import *
from metrics import *
from log import FileLogger
from log import NoLogging
from functools import partial

if __name__ == '__main__':
    logger = FileLogger('game.log')
    redStrat = MinimaxStrategy(4, winHeuristic, logger)
    blueStrat = MinimaxStrategy(4, runHeuristic, logger)
    view = PrintedView()

    game = Game(redStrat, blueStrat, view, logger, startBoard=board)
    # game = Game(MinimaxStrategy(4, runHeuristic, Player.Red), ManualStrategy())
    # game = Game(ManualStrategy(), ManualStrategy())

    game.play()
