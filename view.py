from player import Player, getOpposingPlayer
from board import Board
import os

class View:
    def onWin(self, board: Board, winner: Player):
        pass

    def onPlacePiece(self, board: Board, nextPlayer: Player, placedPiece: int):
        pass

class PrintedView(View):
    def onWin(self, board: Board, winner: Player):
        os.system('cls')
        print(board)

        if (winner == None):
            print("The game was a draw!\n")
        else:
            print(str(winner) + " Wins!!!\n")

    def onPlacePiece(self, board: Board, nextPlayer: Player, placedPiece: int):
        os.system('cls')
        print(board)
        if placedPiece != None:
            print("{} placed a piece in column: {}".format(str(getOpposingPlayer(nextPlayer)), placedPiece))

class NoView(View):
    def onWin(self, board: Board, winner: Player):
        # do nothing
        pass

    def onPlacePiece(self, board: Board, nextPlayer: Player, placedPiece: int):
        # do nothing
        pass
