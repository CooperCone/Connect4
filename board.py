import unittest
from typing import Tuple, List, Iterable, Callable

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
                    row = row + "X"
                elif self.board[x][y] == Player.Blue:
                    row = row + "O"
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

    # (numberOfPlacedTokens, turnsToResolve, List[(x, y)], List[(x, y)])
    # first list is for filled positions, second is for empty positions
    Threat = Tuple[int, int, List[Tuple[int, int]]]

    def getThreats(self) -> Tuple[List[Threat], List[Threat]]:
        def getThreatOnAxis(threats: Tuple[List, List], xRange: Iterable, yRange: Iterable, getRunPosition: Callable[[int, int, int], Tuple[int, int]]):
            # Get all horizontal threats
            foundSlots = set()
            for x in xRange:
                for y in yRange:
                    # check if there is a possible run of two or three that starts here
                    runPositions = [getRunPosition(x, y, i) for i in range(WinRunSize)]
                    numReds, numBlues = (0, 0)
                    emptyPositions = []
                    fullPositions = []
                    for runX, runY in runPositions:
                        if self.board[runX][runY] == Player.Red:
                            numReds += 1
                            fullPositions.append((runX, runY))
                        elif self.board[runX][runY] == Player.Blue:
                            numBlues += 1
                            fullPositions.append((runX, runY))
                        elif self.board[runX][runY] == None:
                            emptyPositions.append((runX, runY))

                    # if there are no reds and no blues, or
                    # both reds and blues, continue
                    if (numReds > 0) == (numBlues > 0):
                        continue
                        
                    # first check if we've already seen a longer run in the same position
                    foundLongerRun = True
                    for position in fullPositions:
                        if position not in foundSlots:
                            foundLongerRun = False
                            break
                    
                    if foundLongerRun:
                        continue

                    # if we're here, then this is a unique run
                    for position in fullPositions:
                        foundSlots.add(position)

                    # so if we're here, that means that either reds
                    # or blues are placed, and not both
                    runPlayer = Player.Red if numReds > 0 else Player.Blue
                    runSize = numReds if runPlayer == Player.Red else numBlues

                    # now look to see how many stones need to be placed to get the win
                    numStonesToPlace = 0
                    placedStones = set()
                    for emptyX, emptyY in emptyPositions:
                        for i in range(emptyY + 1):
                            if self.board[emptyX][i] == None:
                                if (emptyX, i) not in placedStones:
                                    numStonesToPlace += 1
                                    placedStones.add((emptyX, i))

                    threats[int(runPlayer)].append((runSize, numStonesToPlace, fullPositions, emptyPositions))

        threats = ([], [])

        # Get Horizontal Threats
        getThreatOnAxis(threats, range(Width - WinRunSize + 1), range(Height),
            lambda x, y, i: (x + i, y))
        
        # Get Vertical Threats
        getThreatOnAxis(threats, range(Width), range(Height - WinRunSize + 1),
            lambda x, y, i: (x, y + i))

        # Get Right Diagonal Threats
        getThreatOnAxis(threats, range(Width - WinRunSize + 1), range(Height - WinRunSize + 1),
            lambda x, y, i: (x + i, y + i))

        # Get Left Diagonal Threats
        getThreatOnAxis(threats, range(Width - 1, WinRunSize - 1, -1), range(Height - WinRunSize + 1),
            lambda x, y, i: (x - i, y + i))

        return threats

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
                i += 1

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
    # unittest.main()
    board = Board()
    board.deserialize('rrrbeerrrbeerbreeebbeeeerbeeeereeeeereeeee')
    redThreats, blueThreats = board.getThreats()

    print("Board:")
    print(board)
    print("")

    print("Red Threats:")
    for threat in redThreats:
        print("  ", threat)
    
    print("")

    print("Blue Threats:")
    for threat in blueThreats:
        print("  ", threat)
