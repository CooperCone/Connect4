from board import *
from player import *

from copy import deepcopy
from typing import Callable
import logging

class Strategy:
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
    def doTurn(self, board, player, _):
        column = input(str(player) + ": Choose a Column: ")

        text = validateColumn(column, board)
        while text != True:
            print(text)
            column = input("Try again: ")
            text = validateColumn(column, board)

        columnValue = int(column)

        return columnValue


class MinimaxStrategy(Strategy):
    def __init__(self, maxDepth: int, calculateValue: Callable[[Board, Player, int], int], player: Player):
        self.maxDepth = maxDepth
        self.calculateValue = calculateValue
        self.logger = logging.getLogger(f'Minimax_{str(player)}')

    def minimize(self, board: Board, player: Player, turnNumber: int, depth: int):
        depthDiff = (self.maxDepth - depth + 1) * 4
        self.logger.info(' ' * (depthDiff) + f"Minimizing at depth: {depth}")
        if depth == 0:
            self.logger.info(' ' * (depthDiff) + f"Minimize found value of state: {self.calculateValue(board, player, turnNumber)}")
            return (self.calculateValue(board, player, turnNumber), -1)

        # big number, python doesn't have a max value
        minValue = 1e50
        bestCol = -1
        for col in board.getValidColumns():
            self.logger.info(' ' * (depthDiff) + f"Minimize looking at column: {col}")
            newBoard = deepcopy(board)
            newBoard.placePiece(col, getOpposingPlayer(player))

            if newBoard.detectWin() != None:
                return (self.calculateValue(newBoard, player, turnNumber), col)

            (value, _) = self.maximize(newBoard, player, turnNumber + 1, depth - 1)
            if value < minValue:
                minValue = value
                bestCol = col
        self.logger.info(' ' * (depthDiff) + f"Minimize found best value of {minValue} at column {bestCol}")

        return (minValue, bestCol)

    def maximize(self, board: Board, player: Player, turnNumber: int, depth: int):
        depthDiff = (self.maxDepth - depth + 1) * 4
        self.logger.info(' ' * (depthDiff) + f"Maximizing at depth: {depth}")
        if depth == 0:
            self.logger.info(' ' * (depthDiff) + f"Maximize found value of state: {self.calculateValue(board, player, turnNumber)}")
            return (self.calculateValue(board, player, turnNumber), -1)

        maxValue = -1e50
        bestCol = -1
        for col in board.getValidColumns():
            self.logger.info(' ' * (depthDiff) + f"Maximize looking at column: {col}")
            newBoard = deepcopy(board)
            newBoard.placePiece(col, player)

            if newBoard.detectWin() != None:
                return (self.calculateValue(newBoard, player, turnNumber), col)

            (value, _) = self.minimize(newBoard, player, turnNumber + 1, depth - 1)
            if value > maxValue:
                maxValue = value
                bestCol = col
        self.logger.info(' ' * (depthDiff) + f"Maximize found best value of {maxValue} at column {bestCol}")

        return (maxValue, bestCol)

    def doTurn(self, board: Board, player: Player, turnNumber: int):
        self.logger.info("Starting minimax")
        (_, col) = self.maximize(board, player, turnNumber, self.maxDepth)
        print("col: {}".format(col))
        return col
