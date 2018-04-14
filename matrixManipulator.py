import numpy
import random
from scheduleHelpers import Item, Calendar
from pickle import load, dump

def getSquareMatrix(block):
    matrix = []
    day = 96
    if day % block != 0:
        raise ValueError('Please enter a time that can divide into 96 evenly')
    numSegments = int(day/block)
    for column in range(numSegments):
        matrix.append([])
        for row in range(numSegments):
            matrix[column].append('N/A')
    return matrix

def getListofTime(block):
    day = 96
    if day % block != 0:
        raise ValueError('Please enter a time that can divide into 96 evenly')
    else:
        return numpy.linspace(0, day-block, day/block)

def getLongestBlock(itemList):
    longestBlock = 15
    for event in itemList:
        if event.duration > longestBlock:
            longestBlock = event.duration
    return longestBlock
def createItemList(cal):
    itemList = []
    for day in cal.days.values():
        for event in day.events:
            itemList.append(event)



if __name__ == "__main__":
    tempFile = open('testData/willslife', 'rb')
    testCal = load(tempFile)
    toDo = 0
    #testCal.print_days()
    createItemList(testCal)
    print(getSquareMatrix(9))
