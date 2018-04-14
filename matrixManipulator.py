import numpy
import random
from scheduleHelpers import Item, Calendar
from pickle import load, dump

def getSquareMatrix(numBlocks):
    matrix = []
    for column in range(numBlocks):
        matrix.append([])
        for row in range(numBlocks):
            matrix[column].append('N/A')
    return matrix

def getLongestBlock(itemList):
    longestBlock = 15
    for event in itemList:
        if event.duration > longestBlock:
            longestBlock = event.duration
    return longestBlock

print(getSquareMatrix(5))

if __name__ == "__main__":
    tempFile = open('testData/willslife', 'rb')
    testCal = load(tempFile)
    testCal.print_days()
