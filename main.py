from game import Game
from strategy import *
from valueHeuristics import *
from view import *
from log import FileLogger

redStrat = MinimaxStrategy(4, runHeuristic, FileLogger())
blueStrat = MinimaxStrategy(4, runHeuristic, FileLogger())
view = PrintedView()
logger = FileLogger()

game = Game(redStrat, blueStrat, view, logger)
# game = Game(MinimaxStrategy(4, runHeuristic, Player.Red), ManualStrategy())
# game = Game(ManualStrategy(), ManualStrategy())

game.play()
