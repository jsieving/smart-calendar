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

    for x in range(len(itemDuration)):
        if itemDuration[x] == timeBlock:
            retList.append(itemList[x])

    while(len(retList) < len(timeSlots)):
        retList.append('break')
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
            matrix[x][y] = random.randint(0,20)
    return matrix

def main():#will usually call a variable itemList):

    #Segment of code for debugging purposes only
    tempFile = open('testData/willslife', 'rb')
    testCal = load(tempFile)
    testList = getItemList(testCal)
    #del(testList[8])
    itemList = testList
    #above Segmenet for deugging purposes only

    timeBlock = getLongestBlock(itemList)
    timeList = getListofTime(timeBlock)
    taskList = getTaskList(timeList, testList)
    costMatrix = getCostMatrix(len(timeList))
    costMatrix = populateMatrix(timeList, taskList, costMatrix)
    print('list of time slots:', timeList)
    print('list of events:', taskList)
    print('cost matrix:', costMatrix)

    return costMatrix

if __name__ == "__main__":
    tempFile = open('testData/willslife', 'rb')
    testCal = load(tempFile)
    testList = getItemList(testCal)
    #del(testList[8])
    print(testList[8].duration.total_seconds())
    #print(getListofTime(4000))
    # for i in testList:
        # print(i)
    matrix = main()
