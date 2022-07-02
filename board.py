from codecs import charmap_encode
import unittest

from player import Player

WinRunSize = 4
Width = 7
Height = 6

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
                elif self.board[x][y] == Player.Blue:
                    row = row + "B"
                row += " "
            s += "[" + row + "]\n"
        s += "  " + ' '.join([str(i) for i in range(Width)]) + "  \n"

        return s

    def getValidColumns(self):
        cols = []
        for i in range(Width):
            if self.canPlacePiece(i):
                cols.append(i)
        return cols

    def canPlacePiece(self, column: int):
        return self.board[column][Height - 1] == None

    def placePiece(self, column: int, player: Player):
        for y in range(Height):
            if self.board[column][y] == None:
                self.board[column][y] = player
                break
    
    def getVerticalRuns(self, size: int):
        runsOfSize = []
        for x in range(Width):
            curPlayer = None
            curRun = 1
            for y in range(Height):
                if self.board[x][y] == curPlayer:
                    curRun += 1
                else:
                    curPlayer = self.board[x][y]
                    curRun = 1
                
                if curRun == size and curPlayer != None:
                    runsOfSize.append(curPlayer)
                    curPlayer = None
        return runsOfSize

    def getHorizontalRuns(self, size: int):
        runsOfSize = []
        for y in range(Height):
            curPlayer = None
            curRun = 1
            for x in range(Width):
                if self.board[x][y] == curPlayer:
                    curRun += 1
                else:
                    curPlayer = self.board[x][y]
                    curRun = 1
                
                if curRun == size and curPlayer != None:
                    runsOfSize.append(curPlayer)
                    curPlayer = None
        return runsOfSize

    def getUpRightDiagonalRuns(self, size: int):
        runsOfSize = []
        for x in range(Width - 3):
            for y in range(Height - 3):
                player = self.board[x][y]
                for i in range(size):
                    if self.board[x + i][y + i] != player:
                        break

                    if i == size - 1 and player != None:
                        runsOfSize.append(player)
                        break
        return runsOfSize

    def getUpLeftDiagonalRuns(self, size: int):
        runsOfSize = []
        for x in range(Width - 1, 1, -1):
            for y in range(Height - 3):
                player = self.board[x][y]
                for i in range(size):
                    if self.board[x - i][y + i] != player:
                        break

                    if i == size - 1 and player != None:
                        runsOfSize.append(player)
        return runsOfSize

    def getRunsOfSize(self, size: int):
        vertRuns = self.getVerticalRuns(size)
        horizRuns = self.getHorizontalRuns(size)
        rightDiagRuns = self.getUpRightDiagonalRuns(size)
        leftDiagRuns = self.getUpLeftDiagonalRuns(size)

        runs = { Player.Red:0, Player.Blue:0 }
        for lst in [vertRuns, horizRuns, rightDiagRuns, leftDiagRuns]:
            for player in lst:
                runs[player] += 1
        return runs

    def detectWin(self):
        runs = self.getRunsOfSize(WinRunSize)
        redRuns = runs[Player.Red]
        blueRuns = runs[Player.Blue]

        if redRuns > 0:
            return Player.Red
        if blueRuns > 0:
            return Player.Blue

        return None
    
    def serialize(self):
        text = ""
        for x in range(Width):
            for y in range(Height):
                player = self.board[x][y]
                if player == None:
                    text += 'e'
                elif player == Player.Red:
                    text += 'r'
                elif player == Player.Blue:
                    text += 'b'
                else:
                    assert(False)
        return text
                
    def deserialize(self, text):
        i = 0
        for x in range(Width):
            for y in range(Height):
                character = text[i]
                if character == 'e':
                    self.board[x][y] = None
                elif character == 'r':
                    self.board[x][y] = Player.Red
                elif character == 'b':
                    self.board[x][y] = Player.Blue
                else:
                    assert(False)

class BoardTest(unittest.TestCase):
    def testWin(self):
        board = Board()
        board.placePiece(0, Player.Red)
        board.placePiece(0, Player.Red)
        board.placePiece(0, Player.Red)
        board.placePiece(0, Player.Blue)
        board.placePiece(0, Player.Red)
        board.placePiece(0, Player.Red)
        board.placePiece(1, Player.Red)
        board.placePiece(1, Player.Blue)
        board.placePiece(2, Player.Blue)
        board.placePiece(2, Player.Red)
        board.placePiece(2, Player.Blue)
        board.placePiece(2, Player.Blue)
        board.placePiece(3, Player.Blue)
        board.placePiece(3, Player.Blue)
        board.placePiece(3, Player.Red)
        board.placePiece(4, Player.Red)
        board.placePiece(5, Player.Blue)
        self.assertEqual(board.detectWin(), None)

if __name__ == '__main__':
    unittest.main()

