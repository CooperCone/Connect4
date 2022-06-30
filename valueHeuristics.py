from board import *
from player import *

def winHeuristic(board: Board, player: Player, turnNumber: int):
    winRuns = board.getRunsOfSize(WinRunSize)

    if winRuns[getOpposingPlayer(player)] == 1:
        return -1000 - turnNumber
    if winRuns[player] == 1:
        return 1000 - turnNumber
    
    return 0

def runHeuristic(board: Board, player: Player, turnNumber: int):
    allRuns = []
    for i in range(2, WinRunSize + 1):
        allRuns.append((i, board.getRunsOfSize(i)))
    
    finalValue = 0

    for (runSize, runs) in allRuns:
        finalValue += runs[player] * (10 ** runSize)
        finalValue -= runs[getOpposingPlayer(player)] * (10 ** runSize)
    
    return finalValue
