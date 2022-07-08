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

# Threat weights is a tuple of weights for 1, 2, 3, and 4 threats respectively
def threatHeuristic(threatWeights: Tuple[float, float, float, float]):
    def heuristic(board: Board, player: Player, turnNumber: int):
        def getThreatValue(threats):
            threatValue = 0
            for (stonesPlaced, stonesNeeded, _, _) in threats:
                threatValue += threatWeights[stonesPlaced - 1] * (20 - stonesNeeded)
            return threatValue

        (redThreats, blueThreats) = board.getThreats()
        redValue = getThreatValue(redThreats)
        blueValue = getThreatValue(blueThreats)

        if player == Player.Red:
            return redValue - blueValue - turnNumber
        else:
            return blueValue - redValue - turnNumber

    return heuristic
