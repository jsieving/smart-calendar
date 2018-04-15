import numpy
import random
from scheduleHelpers import Item, Calendar
from pickle import load, dump

def getCostMatrix(block):
    matrix = []
    day = 86400
    numSegments = int(day/block)
    for column in range(numSegments):
        matrix.append([])
        for row in range(numSegments):
            matrix[column].append('N/A')
    return matrix

def getTaskList(timeSlots, itemList):
    timeBlock = timeSlots[1] - timeSlots[0]
    itemDuration = []
    retList = []
    for i in range(len(itemList)):
        itemDuration.append(itemList[i].duration.total_seconds())
    for i in range(len(timeSlots)):
        if itemDuration[i] != timeBlock:
            retList.append('break')
        else:
            retList.append(itemList[i])
    return(retList)


def getListofTime(block):
    day = 86400
    if day % block != 0:
        raise ValueError('Please enter a time that can divide into {} evenly'.format(day))
    else:
        return numpy.linspace(0, day-block, day/block)

def getLongestBlock(itemList):
    longestBlock = 900
    for event in itemList:
        if event.duration.total_seconds() > longestBlock:
            longestBlock = event.duration.total_seconds()
    return longestBlock

def getItemList(cal):
    itemList = []
    for day in cal.days.values():
        for event in day.events:
            itemList.append(event)
    return itemList

def main(itemList):
    timeBlock = getLongestBlock(itemList)
    timeList = getListofTime(timeBlock)
    taskList = getTaskList(timeList, testList)
    costMatrix = getCostMatrix(timeBlock)
    print('list of time slots:', timeList)
    print('list of events:', taskList)
    print('cost matrix:', costMatrix)

if __name__ == "__main__":
    tempFile = open('testData/willslife', 'rb')
    testCal = load(tempFile)
    testList = getItemList(testCal)
    del(testList[8])
    main(testList)
