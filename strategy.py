from board import *
from player import *

from copy import deepcopy
from typing import Callable
from log import getLogger

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
        self.logger = getLogger(f'Minimax_{str(player)}')
        self.nodesExplored = 0

    def negamax(self, board: Board, player: Player, turnNumber: int, depth: int):
        self.nodesExplored += 1
        depthDiff = (self.maxDepth - depth + 1) * 4
        self.logger.info(' ' * (depthDiff) + f"Negamaxing at depth: {depth}")
        if depth == 0:
            self.logger.info(' ' * (depthDiff) + f"Negamaxing found value of state: {self.calculateValue(board, player, turnNumber)}")
            return (self.calculateValue(board, player, turnNumber), -1)

        maxValue = -1e50
        bestCol = -1
        for col in board.getValidColumns():
            self.logger.info(' ' * (depthDiff) + f"Negamax looking at column: {col}")
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

    def doTurn(self, board: Board, player: Player, turnNumber: int):
        self.logger.info("Starting minimax")
        # self.nodesExplored = 0
        # (_, col) = self.negamax(board, player, turnNumber, self.maxDepth)
        (_, col) = self.negamaxABPrune(board, player, turnNumber, self.maxDepth, -1e50, 1e50, True)
        # self.logger.info(f"Ended minimax with {self.nodesExplored} nodes explored")
        print("col: {}".format(col))
        return col
