from locale import getlocale
import os

from strategy import Strategy
from player import Player, getOpposingPlayer
from board import Board
from log import getLogger

class Game:
    def __init__(self, redStrategy: Strategy, blueStrategy: Strategy):
        self.redStrat = redStrategy
        self.blueStrat = blueStrategy
        self.board = Board()
        self.prevTurn = None
        self.logger = getLogger('Game')
        self.turnNumber = 1

    def turn(self, strat: Strategy, player: Player):
        self.logger.info(f"New Turn: {str(player)}")
        os.system('cls')

        print(self.board)
        if self.prevTurn != None:
            print("{} placed a piece in column: {}".format(str(getOpposingPlayer(player)), self.prevTurn))
        column = strat.doTurn(self.board, player, self.turnNumber)
        assert(self.board.canPlacePiece(column))
        self.board.placePiece(column, player)
        self.logger.info(f"{str(player)} placed in column {column}")
        self.prevTurn = column

        self.turnNumber += 1

        if self.board.detectWin() == player:
            return True
        
        return False

    def play(self):
        winner = None
        while True:
            if self.turn(self.redStrat, Player.Red):
                winner = Player.Red
                break
            
            if self.turn(self.blueStrat, Player.Blue):
                winner = Player.Blue
                break
        
        os.system('cls')
        print(self.board)

        self.logger.info(f"{str(winner)} won the game")
        print(str(winner) + " Wins!!!\n")
