import numpy
import random
from scheduleHelpers import Item, Calendar
from pickle import load, dump

def getCostMatrix(length):
    matrix = []
    for column in range(length):
        matrix.append([])
        for row in range(length):
            matrix[column].append('N/A')
    return matrix

def getTaskList(timeSlots, itemList):
    timeBlock = timeSlots[1] - timeSlots[0]
    itemDuration = []
    retList = []
    for i in range(len(itemList)):
        itemDuration.append(itemList[i].duration.total_seconds())
    for i in range(len(timeSlots)):
        if itemDuration[i] != timeBlock or i > len(itemList):
            retList.append('break')
        else:
            retList.append(itemList[i])
    return(retList)


def getListofTime(block):
    day = 86400
    if day % block != 0:
        divisions = int(day/block)
        return numpy.linspace(0, block*(divisions), divisions+1)
        #raise ValueError('Please enter a time that can divide into {} evenly'.format(day))
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

def populateMatrix(timeList, taskList, matrix):
    for y in range(len(taskList)):
        for x in range(len(timeList)):
            if x == y:
                matrix[x][y] = 1
            else:
                matrix[x][y] = 0
    return matrix

def main(itemList):
    timeBlock = getLongestBlock(itemList)
    timeList = getListofTime(timeBlock)
    taskList = getTaskList(timeList, testList)
    costMatrix = getCostMatrix(len(timeList))
    costMatrix = populateMatrix(timeList, taskList, costMatrix)
    print('list of time slots:', timeList)
    print('list of events:', taskList)
    print('cost matrix:', costMatrix)

if __name__ == "__main__":
    tempFile = open('testData/willslife', 'rb')
    testCal = load(tempFile)
    testList = getItemList(testCal)
    del(testList[8])
    #print(getListofTime(4000))
    # for i in testList:
        # print(i)
    main(testList)
