import sys

def max_cost(lst):
    maxValue = 0
    for element in lst:
        if sum(element) > maxValue:
            maxValue = sum(element)
    return maxValue

def parseInput():
    finalList = []
    currentList = []
    for line in sys.stdin:
        if line == '\n':
            finalList.append(currentList)
            currentList = []
        else:
            currentList.append(int(line))
    return finalList

def orderByThree(lst):
    sortedList = sorted(lst, reverse=True)
    return (sortedList[0], sortedList[1], sortedList[2])

def parseInputPart2():
    finalList = []
    currentList = []
    for line in sys.stdin:
        if line == '\n':
            finalList.append(sum(currentList))
            currentList = []
        else:
            currentList.append(int(line))
    return finalList

if __name__ == '__main__':
    # Part 1
    # finalList = parseInput()
    # print(max_cost(finalList))
    # Part 2
    finalList = parseInputPart2()
    print(sum(orderByThree(finalList)))
