from locale import getlocale
import os

from strategy import Strategy
from player import Player, getOpposingPlayer
from board import Board
from view import View
from log import getLogger

class Game:
    def __init__(self, redStrategy: Strategy, blueStrategy: Strategy, view: View, startBoard: Board = None):
        self.redStrat = redStrategy
        self.redStrat.setPlayer(Player.Red)
        self.blueStrat = blueStrategy
        self.blueStrat.setPlayer(Player.Blue)
        self.board = Board() if startBoard == None else startBoard
        self.view = view
        self.prevTurn = None
        self.logger = getLogger('Game')
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
            if self.turn(self.redStrat, Player.Red):
                winner = Player.Red
                break
            
            if self.turn(self.blueStrat, Player.Blue):
                winner = Player.Blue
                break
            
            curTurn += 1
        
        self.view.onWin(self.board, winner)
        self.logger.info(f"{str(winner)} won the game")
