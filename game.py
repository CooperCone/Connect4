from enum import Enum
from abc import ABC
import os

Width = 7
Height = 6

class Player(Enum):
    Red = 1
    Black = 2

    def __str__(self):
        return self.name

class Board:
    def __init__(self):
        self.board = [[None for y in range(Height)] for x in range(Width)]
    
    def __str__(self):
        s = "\r"
        for y in range(Height - 1, -1, -1):
            row = " "
            for x in range(Width):
                if self.board[x][y] == None:
                    row = row + " "
                elif self.board[x][y] == Player.Red:
                    row = row + "R"
                elif self.board[x][y] == Player.Black:
                    row = row + "B"
                row += " "
            s += "[" + row + "]\n"
        s += "  " + ' '.join([str(i) for i in range(Width)]) + "  \n"

        return s

    def canPlacePiece(self, column):
        return self.board[column][Height - 1] == None

    def placePiece(self, column, player):
        for y in range(Height):
            if self.board[column][y] == None:
                self.board[column][y] = player
                break
    
    def detectWin(self):
        # detect vertical wins
        for x in range(Width):
            curPlayer = None
            curRun = 1
            for y in range(Height):
                if self.board[x][y] == curPlayer:
                    curRun += 1
                else:
                    curPlayer = self.board[x][y]
                    curRun = 1
                
                if curRun == 4 and curPlayer != None:
                    return curPlayer
        
        # detect horizontal wins
        for y in range(Height):
            curPlayer = None
            curRun = 1
            for x in range(Width):
                if self.board[x][y] == curPlayer:
                    curRun += 1
                else:
                    curPlayer = self.board[x][y]
                    curRun = 1
                
                if curRun == 4 and curPlayer != None:
                    return curPlayer
        
        # detect up right diagonal wins
        for x in range(Width - 3):
            for y in range(Height - 3):
                player = self.board[x][y]
                for i in range(4):
                    if self.board[x + i][y + i] != player:
                        break

                    if i == 3:
                        return player

        # detect up left diagonal wins
        for x in range(Width - 1, 1, -1):
            for y in range(Height - 1, 1, -1):
                player = self.board[x][y]
                for i in range(4):
                    if self.board[x - i][y - i] != player:
                        break

                    if i == 3:
                        return player

        return None

class Strategy:
    def doTurn(self, board):
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
    def doTurn(self, board, name):
        column = input(name + ": Choose a Column: ")

        text = validateColumn(column, board)
        while text != True:
            print(text)
            column = input("Try again: ")
            text = validateColumn(column, board)

        columnValue = int(column)

        return columnValue

class Game:
    def __init__(self, redStrategy, blackStrategy):
        self.redStrat = redStrategy
        self.blackStrat = blackStrategy
        self.board = Board()

    def turn(self, strat, player):
        os.system('cls')

        print(self.board)
        column = strat.doTurn(self.board, str(player))
        assert(self.board.canPlacePiece(column))
        self.board.placePiece(column, player)

        if self.board.detectWin() == player:
            print(str(player) + " Wins!!!\n")
            return True
        
        return False

    def play(self):
        while True:
            if self.turn(self.redStrat, Player.Red):
                break
            
            if self.turn(self.redStrat, Player.Black):
                break
