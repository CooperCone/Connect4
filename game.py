from locale import getlocale
import os

from strategy import Strategy
from player import Player, getOpposingPlayer
from board import Board
from view import View
from log import LoggingStrategy

class Game:
    def __init__(self, redStrategy: Strategy, blueStrategy: Strategy, view: View, logging: LoggingStrategy, startBoard: Board = None):
        self.redStrat = redStrategy
        self.redStrat.setPlayer(Player.Red)
        self.blueStrat = blueStrategy
        self.blueStrat.setPlayer(Player.Blue)
        self.board = Board() if startBoard == None else startBoard
        self.logger = logging.getLogger('Game')
        self.view = view
        self.prevTurn = None
        self.turnNumber = 1

    def turn(self, strat: Strategy, player: Player):
        self.logger.info(f"New Turn: {str(player)}")
        
        self.view.onPlacePiece(self.board, player, self.prevTurn)

        column = strat.doTurn(self.board, self.turnNumber)
        assert(self.board.canPlacePiece(column))
        self.board.placePiece(column, player)
        self.logger.info(f"{str(player)} placed in column {column}")
        self.prevTurn = column

        self.turnNumber += 1

        if self.board.detectWin() == player:
            return True
        
        return False

    def play(self, maxTurns = None):
        winner = None
        curTurn = 0
        while maxTurns == None or curTurn < maxTurns:
            if len(self.board.getValidColumns()) == 0:
                break
            
            if self.turn(self.redStrat, Player.Red):
                winner = Player.Red
                break
            
            if len(self.board.getValidColumns()) == 0:
                break

            if self.turn(self.blueStrat, Player.Blue):
                winner = Player.Blue
                break
            
            curTurn += 1

        # TODO: Fix this!
        if winner == None:
            self.redStrat.reportMetric("win", 0)
            self.redStrat.reportMetric("loss", 0)
            self.blueStrat.reportMetric("win", 0)
            self.blueStrat.reportMetric("loss", 0)
        elif winner == Player.Red:
            self.redStrat.reportMetric("win", 1)
            self.redStrat.reportMetric("loss", 0)
            self.blueStrat.reportMetric("win", 0)
            self.blueStrat.reportMetric("loss", 1)
        elif winner == Player.Blue:
            self.redStrat.reportMetric("win", 0)
            self.redStrat.reportMetric("loss", 1)
            self.blueStrat.reportMetric("win", 1)
            self.blueStrat.reportMetric("loss", 0)
        else:
            assert(False)

        if winner == None:
            self.logger.info("The game was a draw")
        else:
            self.logger.info(f"{str(winner)} won the game")
        self.view.onWin(self.board, winner)
