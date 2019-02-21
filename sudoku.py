import copy
from numpy import sqrt, zeros, array_equal
import sys
import random


class Sudoku:
    def __init__(self, input):
        self.sudoku = input


class Path:
    def __init__(self):
        self.states = []
        self.cost = 0
        self.explored = False
        self.solvable = True

    def __eq__(self, other):
        if isinstance(other, Path):
            return array_equal(self.states, other.states)
        return False


class Action:
    def __init__(self, number, x, y):
        self.number = number
        self.xCoordinate = x
        self.yCoordinate = y

#Method to check if a row in the sudoku is completed
def checkRow(sudoku, row, n, x):
    numbers = []
    max = int(sqrt(sudoku.size))
    defaultSum = 0
    for i in range(max):
        defaultSum = defaultSum + i + 1

    for i in range(n):
        if int(sudoku[row, i]) != 0:
            numbers.append(sudoku[row, i])
    if x in numbers:
        sum = 0
        for i in range(len(numbers)):
            sum = sum + numbers[i]

        if defaultSum == sum:
            return True
        else:
            return False
    else:
        return False


def checkColumn(sudoku, column, n, x):
    numbers = []
    max = int(sqrt(sudoku.size))
    defaultSum = 0
    for i in range(max):
        defaultSum = defaultSum + i + 1

    for j in range(n):
        if int(sudoku[j, column]) != 0:
            numbers.append(sudoku[j, column])
    if x in numbers:
        sum = 0
        for i in range(len(numbers)):
            sum = sum + numbers[i]

        if defaultSum == sum:
            return True
        else:
            return False
    else:
        return False


def checkBox(sudoku, row, column, n, x):
    numbers = []
    max = int(sqrt(sudoku.size))
    defaultSum = 0
    for i in range(max):
        defaultSum = defaultSum + i + 1

    if (row < 2):
        if (column < 2):
            numbers.append(sudoku[0, 0])
            numbers.append(sudoku[0, 1])
            numbers.append(sudoku[1, 0])
            numbers.append(sudoku[1, 1])
        else:
            numbers.append(sudoku[0, 2])
            numbers.append(sudoku[0, 3])
            numbers.append(sudoku[1, 2])
            numbers.append(sudoku[1, 3])
    else:
        if (column < 2):
            numbers.append(sudoku[2, 0])
            numbers.append(sudoku[2, 1])
            numbers.append(sudoku[3, 0])
            numbers.append(sudoku[3, 1])
        else:
            numbers.append(sudoku[2, 2])
            numbers.append(sudoku[2, 3])
            numbers.append(sudoku[3, 2])
            numbers.append(sudoku[3, 3])
    if (x in numbers):
        sum = 0
        for i in range(len(numbers)):
            sum = sum + numbers[i]

        if defaultSum == sum:
            return True
        else:
            return False
    else:
        return False


def statWeight(sudoku, n):
    weight: int = 0
    for x in n:
        for y in n:
            if (int(sudoku[x][y]) != 0):
                weight = weight + 1
    return weight


def pathCost(path):
    cost = 0
    for state in path.states:
        cost = cost + 1
    return cost


def rowOrColumnComplete(row):
    for x in range(len(row)):
        if row[x] == 0:
            return False
    return True


def heurisic(s):
    rowsAndColumnsCompleted = 0
    quadrantsCompleted = 0
    max = int(sqrt(s.size))

    # Cheking amount of rows and columns completed
    for i in range(max):
        if rowOrColumnComplete(s[i]):
            rowsAndColumnsCompleted = rowsAndColumnsCompleted + 1

    for j in range(max):
        column = []
        for i in range(max):
            column.append(s[i][j])
        if rowOrColumnComplete(column):
            rowsAndColumnsCompleted = rowsAndColumnsCompleted + 1

    if s[0][0] != 0 and s[0][1] != 0 and s[1][0] != 0 and s[1][1] != 0:
        quadrantsCompleted = quadrantsCompleted + 1

    if s[2][0] != 0 and s[2][1] != 0 and s[3][0] != 0 and s[3][1] != 0:
        quadrantsCompleted = quadrantsCompleted + 1

    if s[0][2] != 0 and s[0][3] != 0 and s[1][2] != 0 and s[1][3] != 0:
        quadrantsCompleted = quadrantsCompleted + 1

    if s[2][2] != 0 and s[2][3] != 0 and s[3][2] != 0 and s[3][3] != 0:
        quadrantsCompleted = quadrantsCompleted + 1

    return rowsAndColumnsCompleted + quadrantsCompleted


def criteria(frontier, minCost):
    resPath = Path()
    newFrontier = []
    for path in frontier:
        if path.solvable:
            cost = pathCost(path)
            path.cost = cost + heurisic(path.states[len(path.states) - 1])
            if path.cost > minCost:
                minCost = path.cost
                resPath = path
            newFrontier.append(path)
    frontier = copy.deepcopy(newFrontier)
    if len(resPath.states) == 0:
        resPath = random.choice(frontier)
    return resPath


def goalTest(s):
    max = int(sqrt(s.size))
    for i in range(max):
        for j in range(max):
            if not checkBox(s, i, j, max, s[i][j]):
                return False
            if not checkRow(s, i, max, s[i][j]):
                return False
            if not checkColumn(s, j, max, s[i][j]):
                return False
    return True


def getRow(s, row):
    numbers = s[row]
    return numbers


def getColumn(s, column):
    numbers = []
    max = int(sqrt(s.size))
    for i in range(max):
        numbers.append(s[i][column])
    return numbers


def getQuadrant(s, row, column):
    numbers = []
    if (row < 2):
        if (column < 2):
            numbers.append(s[0, 0])
            numbers.append(s[0, 1])
            numbers.append(s[1, 0])
            numbers.append(s[1, 1])
        else:
            numbers.append(s[0, 2])
            numbers.append(s[0, 3])
            numbers.append(s[1, 2])
            numbers.append(s[1, 3])
    else:
        if (column < 2):
            numbers.append(s[2, 0])
            numbers.append(s[2, 1])
            numbers.append(s[3, 0])
            numbers.append(s[3, 1])
        else:
            numbers.append(s[2, 2])
            numbers.append(s[2, 3])
            numbers.append(s[3, 2])
            numbers.append(s[3, 3])
    return numbers


def actions(s):
    possibleActions = []
    max = int(sqrt(s.size))
    values = []
    for i in range(max):
        values.append(i + 1)

    for i in range(max):
        for j in range(max):
            if (s[i][j] == 0):
                possibleValues = list(set(values) - set(getColumn(s, j)))
                possibleValues = list(set(possibleValues) - set(getRow(s, i)))
                possibleValues = list(set(possibleValues) - set(getQuadrant(s, i, j)))
                for p in range(len(possibleValues)):
                    action = Action(possibleValues[p], i, j)
                    possibleActions.append(action)
    return possibleActions


def result(s, a):
    newS = copy.deepcopy(s)
    newS[a.xCoordinate][a.yCoordinate] = a.number
    return newS


def isExplored(path, res, explored):
    newPath = copy.deepcopy(path)
    newPath.states.append(res)

    if newPath in explored:
        return True
    else:
        return False

def isSolvable(path, response, explored):
    newPath = copy.deepcopy(path)
    newPath.states.append(response)

    if newPath in explored:
        path.solvable = False
        return False
    else:
        return True



def graph_search(sudoku):
    frontier = []
    explored = []
    values = []
    possibleActions = []

    # Creating an array of possible sudoku values
    for x in range(n):
        values.append(x + 1)

    # Creating a new sudoku type object as a new state.
    state = sudoku
    initialPath = Path()
    initialPath.states.append(state)

    frontier.append(initialPath)
    minCost = pathCost(initialPath)

    count = 0
    while True:
        if count > 1000 :
            return "Lo lamento, no pude encontrar una solución a tu sudoku."
        else:
            path = criteria(frontier, minCost)
            s = copy.deepcopy(path.states[len(path.states) - 1])
            print("Moviemiento #" , count, ":\n", s, "\n")
            path.explored = True
            explored.append(path)

            if (goalTest(s)):
                return s

            possibleActions = actions(s)
            if len(possibleActions) == 0:
                path.solvable = False

            newActions = []
            for a in possibleActions:
                response = result(s, a)
                if isSolvable(path, response, explored):
                    newActions.append(a)

            for a in newActions:
                response = result(s, a)

                if not isExplored(path, response, explored):
                    newPath = copy.deepcopy(path)
                    newPath.states.append(response)
                    frontier.append(newPath)
        count = count + 1

# Cleaning the incoming input
input = sys.argv[1]
input = input.split('=')
input = input[1]
print("This is the input: ", input)

# Obtaining input size to know what n x n size is the sudoku, where n is the input size.
inputSize = len(input)
n = sqrt(inputSize)
n = int(n)

# Creating a n x n sudoku filled with zeros
sudoku = zeros((n, n))

# Filling the sudoku with the input
characters = input
for x in range(n):
    for y in range(n):
        if characters[0] != ".":
            sudoku[x, y] = characters[0]
        characters = characters[1:]

print(sudoku)

print("El resultado es: \n", graph_search(sudoku))
