from typing import Tuple
from multiprocessing.dummy import freeze_support
from game import Game
from metrics import *
from strategy import *
from board import *
from metrics import *
from view import NoView
from log import NoLogging
from log import FileLogger
from valueHeuristics import runHeuristic, threatHeuristic, winHeuristic

import time
import copy
import multiprocessing

Run = Tuple[Tuple[str, str], Tuple[Strategy, Strategy]]

class Simulator:
    def __init__(self):
        self.strategies: List[Tuple[str, Strategy]] = []
        self.logger = FileLogger('simulation.log').getLogger("Simulator")

    def addStrategy(self, name: str, strat: Strategy):
        self.strategies.append((name, strat))

    def createRuns(self) -> List[Run]:
        runs: List[Run] = []
        for i in range(len(self.strategies)):
            for ii in range(i + 1, len(self.strategies)):
                firstName, firstStrat = self.strategies[i]
                secondName, secondStrat = self.strategies[ii]
                runs.append(((firstName, secondName), (copy.deepcopy(firstStrat), copy.deepcopy(secondStrat))))
                runs.append(((secondName, firstName), (copy.deepcopy(secondStrat), copy.deepcopy(firstStrat))))
        return runs

    # TODO: Should we send in text instead of filename?
    def simulateRun(self, run: Run, simulationFilename: str) -> MetricList:
        (redName, blueName), (redStrat, blueStrat) = run
        metrics: MetricList = []
        self.logger.info(f"Starting simulate run with {redName} and {blueName}")
        index = 0
        with open(simulationFilename, 'r') as file:
            for line in file.readlines():
                self.logger.info(f"  [{redName} vs {blueName}] Run {index}: {line[:-1]}")
                startBoard = Board()
                startBoard.deserialize(line)
                redStrat.metrics = {}
                blueStrat.metrics = {}
                Game(redStrat, blueStrat, NoView(), NoLogging(), startBoard=copy.deepcopy(startBoard)).play()

                metrics.append((redStrat.metrics, blueStrat.metrics))
                index += 1
        return metrics

    # TODO: update with types and make this work
    # def simulateMultiProcess(self, simulationFilename, evaluationMetrics):
    #     assert(len(self.strategies) > 1)

    #     runs = self.createRuns()

    #     pool = multiprocessing.Pool(processes=1)
    #     args = [(run, simulationFilename) for run in runs]
    #     mets = pool.starmap(self.simulateRun, args)

    #     print(mets)

    #     allMetrics = []
    #     for metrics, run in zip(mets, runs):
    #         (redName, blueName) = run[0]
    #         combinedMetrics = evaluationMetrics(metrics)
    #         allMetrics.append(((redName, blueName), combinedMetrics))

    #     return allMetrics

    def simulate(self, simulationFilename: str, evaluationMetrics: Callable[[MetricList], List[MetricReport]]) -> List[RunReport]:
        assert(len(self.strategies) > 1)

        runs: List[Run] = self.createRuns()

        allMetrics: RunReport = []
        for run in runs:
            (redName, blueName) = run[0]
            metrics: MetricList = self.simulateRun(run, simulationFilename)
            print("Here")
            for i in range(len(metrics)):
                if "time" not in metrics[i][0]:
                    print(i, "red")
                if "time" not in metrics[i][1]:
                    print(i, "blue")
            combinedMetrics: List[MetricReport] = evaluationMetrics(metrics)
            allMetrics.append(((redName, blueName), combinedMetrics))

        return allMetrics

    def expand(self, string, length):
        assert(len(string) < length)
        return string + " " * (length - len(string))

    def printSimuationResults(self, metrics: List[RunReport]):
        # First combine runs
        CombinableMetrics = Tuple[List[ReportValue], List[ReportValue]]
        combinedRunMetrics : Dict[str, Dict[str, CombinableMetrics]] = {}
        combiners : Dict[str, MetricRunCombinator] = {}
        toStrs : Dict[str, ToString] = {}
        for (redName, blueName), metricReportList in metrics:
            if redName not in combinedRunMetrics:
                combinedRunMetrics[redName] = {}
            if blueName not in combinedRunMetrics:
                combinedRunMetrics[blueName] = {}

            for metricName, toStr, combiner, (redValue, blueValue) in metricReportList:
                if metricName not in combiners:
                    combiners[metricName] = combiner
                if metricName not in toStrs:
                    toStrs[metricName] = toStr
                
                if metricName not in combinedRunMetrics[redName]:
                    combinedRunMetrics[redName][metricName] = ([redValue], [])
                else:
                    combinedRunMetrics[redName][metricName][0].append(redValue)
                
                if metricName not in combinedRunMetrics[blueName]:
                    combinedRunMetrics[blueName][metricName] = ([], [blueValue])
                else:
                    combinedRunMetrics[blueName][metricName][1].append(blueValue)

        algoSlots = 20
        algoTitle = self.expand("Algorithm", algoSlots)
        metricSlots = 20
        metricTitle = self.expand("Metric", metricSlots)
        valueSlots = 15
        redTitle = self.expand("Red Value", valueSlots)
        blueTitle = self.expand("Blue Value", valueSlots)
        print(f"{algoTitle}{metricTitle}{redTitle}{blueTitle}")

        for algoName, combinableMetrics in combinedRunMetrics.items():
            print(f"{self.expand(algoName, algoSlots)}", end="")

            first = True
            for metricName, reportValues in combinableMetrics.items():
                combineFunc = combiners[metricName]
                redValue, blueValue = combineFunc(reportValues)

                if not first:
                    print(" " * algoSlots, end="")
                else:
                    first = False

                toStr = toStrs[metricName]

                print(f"{self.expand(metricName, metricSlots)}", end="")
                print(f"{self.expand(toStr(redValue), valueSlots)}", end="")
                print(f"{self.expand(toStr(blueValue), valueSlots)}")

simulator = Simulator()
# simulator.addStrategy("Random", RandomStrategy(seed=5))
simulator.addStrategy("Minimax(4,run)", MinimaxStrategy(4, runHeuristic))
simulator.addStrategy("Minimax(4,threat)", MinimaxStrategy(4, threatHeuristic((1, 10, 100, 100000))))
# simulator.addStrategy(MinimaxStrategy(5, runHeuristic, NoLogging()))
# simulator.addStrategy(MinimaxStrategy(5, winHeuristic, NoLogging()))

calcMetrics = lambda metrics: [
    metric_create("Wins",
        lambda x: f"{x:d}",
        metric_sum,
        metric_sum(
            metric_flatten(
                metric_collect(metrics, "win")
            )
        )
    ),
    metric_create("Losses",
        lambda x: f"{x:d}",
        metric_sum,
        metric_sum(
            metric_flatten(
                metric_collect(metrics, "loss")
            )
        )
    ),
    metric_create("Turn Time",
        lambda x: f"{x:.4f}",
        metric_avg,
        metric_avg(
            metric_map(
                metric_collect(metrics, "time"),
                metric_median
            )
        )
    ),
]

# tic = time.perf_counter()
metrics: List[RunReport] = simulator.simulate('randomTests_50.test', calcMetrics)
simulator.printSimuationResults(metrics)
# toc = time.perf_counter()
