from game import Game
from strategy import *
from board import *
from view import NoView
from valueHeuristics import runHeuristic, winHeuristic

import copy

# pit all of the strategies against each other

strategies = [
    RandomStrategy(seed=5),
    MinimaxStrategy(4, winHeuristic),
    MinimaxStrategy(4, runHeuristic),
    MinimaxStrategy(5, runHeuristic),
    MinimaxStrategy(5, winHeuristic),
]

pairs = []
for i in range(len(strategies)):
    for ii in range(i + 1, len(strategies)):
        pairs.append((copy.deepcopy(strategies[i]), copy.deepcopy(strategies[ii])))

print(len(pairs))

for pair in pairs:
    with open('randomTests.test', 'r') as file:
        for line in file.readlines():
            startBoard = Board()
            startBoard.deserialize(line)

            print("Starting Game")
            Game(pair[0], pair[1], NoView(), startBoard=copy.deepcopy(startBoard)).play()
            print("Starting Game")
            Game(pair[1], pair[0], NoView(), startBoard=copy.deepcopy(startBoard)).play()
