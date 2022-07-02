from game import Game
from strategy import *
from valueHeuristics import *
import log

log.setupLogger()
logger = log.getLogger('Main')

redStrat = MinimaxStrategy(4, runHeuristic, Player.Red)
blueStrat = MinimaxStrategy(4, runHeuristic, Player.Blue)

game = Game(redStrat, blueStrat)
# game = Game(MinimaxStrategy(4, runHeuristic, Player.Red), ManualStrategy())
# game = Game(ManualStrategy(), ManualStrategy())

game.play()

logger.info(f"Red nodes: {redStrat.nodesExplored}")
logger.info(f"Blue nodes: {redStrat.nodesExplored}")
