import numpy
import random

def getSquareMatrix(numBlocks):
    matrix = []
    for column in range(numBlocks):
        matrix.append([])
        for row in range(numBlocks):
            matrix[column].append('N/A')
    return matrix

def getLongestBlock():
    pass

print(getSquareMatrix(5))
