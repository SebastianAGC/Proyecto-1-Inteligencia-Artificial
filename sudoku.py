import numpy as np
import sys

def checkRowOrColumn(sudoku, row, column, n, x):
    numbers = []
    for row in n:
        for column in n:
            numbers.append(sudoku[row, column])
    if(x in numbers):
        return True
    else:
        return False

def checkBox(sudoku, row, column, n, x):
    pass



print('This is the sudoku given: ', sys.argv[1])

#Cleaning the incoming input
input = sys.argv[1]
print(input)
input = input.split('=')
print(input)

#Final input
input = input[1]
print("This is the input: ", input)

#Obtaining input size to know what n x n size, where n is the input size.
inputSize = len(input)
n = np.sqrt(inputSize)
n = int(n)

#Creating a n x n sudoku filled with zeros
sudoku = np.zeros((n,n))

#
characters = input
for x in range (n):
    for y in range(n):
        if(characters[0] != "."):
            sudoku[x, y] = characters[0]
        characters = characters[1:]

print(sudoku)
