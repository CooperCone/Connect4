from game import Game
from strategy import *
from valueHeuristics import *
from view import *
from metrics import *
from log import FileLogger
from log import NoLogging
from functools import partial

# redStrat = ManualStrategy()
redStrat = MinimaxStrategy(4, runHeuristic, FileLogger())
blueStrat = MinimaxStrategy(4, runHeuristic, NoLogging())
view = PrintedView()
logger = NoLogging()

game = Game(redStrat, blueStrat, view, logger)
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
