from board import *
from player import *

from copy import deepcopy
from typing import Callable
from log import LoggingStrategy, NoLogging
import random
import time

class Strategy:
    def __init__(self):
        self.metrics = {}

    def setPlayer(self, player):
        self.player = player

    def reportMetric(self, name, value):
        if not name in self.metrics:
            self.metrics[name] = [ value ]
        else:
            self.metrics[name].append(value)

    def doTurn(self, board, player, turnNumber):
        pass

def validateColumn(column, board):
    if not column.isnumeric():
        return "Sorry, you need to input a number.\n"
    
    value = int(column)
    if value < 0 or value > Width - 1:
        return "Sorry, your column number must be between 0 and {}.\n".format(Width - 1)

    if not board.canPlacePiece(value):
        return "Sorry, you can't place a piece in a column that is full.\n"
    
    return True


class ManualStrategy(Strategy):
    def doTurn(self, board, _):
        tic = time.perf_counter()

        column = input(str(self.player) + ": Choose a Column: ")

        text = validateColumn(column, board)
        while text != True:
            print(text)
            column = input("Try again: ")
            text = validateColumn(column, board)

        columnValue = int(column)

        toc = time.perf_counter()
        self.reportMetric("time", toc - tic)

        return columnValue

class RandomStrategy(Strategy):
    def __init__(self, seed = None):
        super(RandomStrategy, self).__init__()
        if seed != None:
            random.seed(seed)
        self.metrics = {}
    
    def doTurn(self, board: Board, _):
        tic = time.perf_counter()
        
        col = random.randrange(Width)
        while not board.canPlacePiece(col):
            col = random.randrange(Width)
        
        toc = time.perf_counter()
        self.reportMetric("time", toc - tic)

        return col

class MinimaxStrategy(Strategy):
    def __init__(self, maxDepth: int, calculateValue: Callable[[Board, Player, int], int], logging: LoggingStrategy = NoLogging()):
        super(MinimaxStrategy, self).__init__()
        self.maxDepth = maxDepth
        self.calculateValue = calculateValue
        self.nodesExplored = 0
        self.logging = logging
    
    def setPlayer(self, player):
        self.player = player
        self.logger = self.logging.getLogger(f'Minimax_{str(player)}')

    def negamax(self, board: Board, player: Player, turnNumber: int, depth: int):
        self.nodesExplored += 1
        depthDiff = (self.maxDepth - depth + 1) * 4
        self.logger.info(' ' * (depthDiff) + f"Negamaxing at depth: {depth}")
        if depth == 0:
            self.logger.info(' ' * (depthDiff) + f"Negamaxing found value of state: {self.calculateValue(board, player, turnNumber)}")
            return (self.calculateValue(board, player, turnNumber), -1)

        maxValue = -1e50
        bestCol = -1
        self.logger.info(' ' * depthDiff + 'Valid Columns: ')
        for col in board.getValidColumns():
            newBoard = deepcopy(board)
            newBoard.placePiece(col, player)

            if newBoard.detectWin() != None:
                return (self.calculateValue(newBoard, player, turnNumber), col)

            (value, _) = self.negamax(newBoard, getOpposingPlayer(player), turnNumber + 1, depth - 1)
            value *= -1
            if value > maxValue:
                maxValue = value
                bestCol = col
        self.logger.info(' ' * (depthDiff) + f"Negamax found best value of {maxValue} at column {bestCol}")

        return (maxValue, bestCol)

    def negamaxABPrune(self, board: Board, player: Player, turnNumber: int, depth: int, alpha: int, beta: int, isMaximizing: bool):
        self.nodesExplored += 1
        depthDiff = (self.maxDepth - depth + 1) * 4
        self.logger.info(' ' * (depthDiff) + f"Negamaxing at depth: {depth}")
        if depth == 0:
            self.logger.info(' ' * (depthDiff) + f"Negamaxing found value of state: {self.calculateValue(board, player, turnNumber)}")
            return (self.calculateValue(board, player, turnNumber), -1)

        maxValue = -1e50
        bestCol = -1
        validColumns = board.getValidColumns()
        self.logger.info(' ' * depthDiff + 'Valid Columns: ' + str(validColumns))
        assert(len(validColumns) >= 1)
        if len(validColumns) == 1:
            self.logger.info(' ' * depthDiff + 'Only one valid move: ' + str(validColumns[0]))
            return (maxValue, validColumns[0])

        for col in board.getValidColumns():
            self.logger.info(' ' * (depthDiff) + f"Negamax looking at column: {col}")
            newBoard = deepcopy(board)
            newBoard.placePiece(col, player)

            if newBoard.detectWin() != None:
                return (self.calculateValue(newBoard, player, turnNumber), col)

            (value, _) = self.negamaxABPrune(newBoard, getOpposingPlayer(player), turnNumber + 1, depth - 1, -beta, -alpha, not isMaximizing)
            value *= -1
            if value > maxValue:
                maxValue = value
                bestCol = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        self.logger.info(' ' * (depthDiff) + f"Negamax found best value of {maxValue} at column {bestCol}")

        return (maxValue, bestCol)

    def doTurn(self, board: Board, turnNumber: int):
        tic = time.perf_counter()
        self.logger.info("Starting minimax")
        # (_, col) = self.negamax(board, player, turnNumber, self.maxDepth)
        (_, col) = self.negamaxABPrune(board, self.player, turnNumber, self.maxDepth, -1e50, 1e50, True)
        toc = time.perf_counter()
        self.reportMetric("time", toc - tic)
        return col
