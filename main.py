from game import Game
from strategy import *
from valueHeuristics import *
from view import *
from metrics import *
from log import FileLogger
from log import NoLogging
from functools import partial

logger = FileLogger('game.log')
redStrat = MinimaxStrategy(4, winHeuristic, logger)
blueStrat = MinimaxStrategy(4, runHeuristic, logger)
view = PrintedView()

board = Board()
board.deserialize("eeeeeebeeeeerbrbeeeeeeeereeeeeeeeeeeeeeeee")

game = Game(redStrat, blueStrat, view, logger, startBoard=board)
# game = Game(MinimaxStrategy(4, runHeuristic, Player.Red), ManualStrategy())
# game = Game(ManualStrategy(), ManualStrategy())

game.play()

metrics = ([redStrat.metrics], [blueStrat.metrics])

combinedMetrics = [
    metric_label("Turn Time",
        metric_avg(
            metric_map(
                metric_get(metrics, "time"),
                metric_avg
            )
        )
    )
]

printMetrics(combinedMetrics)
