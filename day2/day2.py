import sys

def parseStrategyGuide():
    finalList = []
    for line in sys.stdin:
        (opponentMove, yourMove) = line.split()
        finalList.append((opponentMove, yourMove))
    return finalList

def perGameScore(player, opponent):
    if opponent == 'A':
        if player == 'X':
            return 4
        elif player == 'Y':
            return 8
        elif player == 'Z':
            return 3
    elif opponent == 'B':
        if player == 'X':
            return 1
        elif player == 'Y':
            return 5
        elif player == 'Z':
            return 9
    elif opponent == 'C':
        if player == 'X':
            return 7
        elif player == 'Y':
            return 2
        elif player == 'Z':
            return 6
    print(f'NoneType reached: Opponent: {opponent}, Player: {player}')
        
def calculateScore(lst):
    score = 0
    for element in lst:
        (opponentMove, yourMove) = element
        score += perGameScore(yourMove, opponentMove)
    return score

def figureYourMove(opponentMove, result):
    if opponentMove == 'A':
        if result == 'X':
            return 'Z'
        elif result == 'Y':
            return 'X'
        elif result == 'Z':
            return 'Y'
    elif opponentMove == 'B':
        if result == 'X':
            return 'X'
        elif result == 'Y':
            return 'Y'
        elif result == 'Z':
            return 'Z'
    elif opponentMove == 'C':
        if result == 'X':
            return 'Y'
        elif result == 'Y':
            return 'Z'
        elif result == 'Z':
            return 'X'

def calculateScoreRound2(lst):
    score = 0
    for element in lst:
        (opponentMove, result) = element
        yourMove = figureYourMove(opponentMove=opponentMove, result=result)
        score += perGameScore(yourMove, opponentMove)
    return score

if __name__ == '__main__':
    finalList = parseStrategyGuide()
    # Part 1
    print(f'Part 1: {calculateScore(finalList)}')
    # Part 2
    print(f'Part 2: {calculateScoreRound2(finalList)}')
