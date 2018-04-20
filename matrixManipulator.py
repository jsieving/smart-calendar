'''
Created by Jane, Vienna, Micah, Will on 4/15/17

This file contains functions for creating and manipulating cost matrices.
-> The axes are defined by a list of time slots and a list of tasks
'''
import numpy
import random
from scheduleHelpers import Item, Calendar
from pickle import load, dump


def getCostMatrix(length):
    """
    Creates a square matrix.

    length: dimensions of matrix

    return: square matrix with dimensions lengthXlength
    """
    matrix = []
    for column in range(length):
        matrix.append([])
        for row in range(length):
            matrix[column].append('N/A')
    return matrix

def getTaskList(timeSlots, itemList):
    """
    Creates a list of tasks that form the y-axis of the cost-matrix.

    timeSlots: list of timeslots in cost-matrix
    itemList: list of items that need to be scheduled

    return: A list of items that have the same duration as the time
    slots. To maintain the same length as timeSlots, the return list includes fake
    events labeled 'break'.
    """
    timeBlock = timeSlots[1] - timeSlots[0]
    itemDuration = []
    retList = []
    for i in range(len(itemList)):
        itemDuration.append(itemList[i].duration.total_seconds()/60)

    for x in range(len(itemDuration)):
        if itemDuration[x] == timeBlock:
            retList.append(itemList[x])

    #should probably include an error message if while loop gets too large.
    while(len(retList) < len(timeSlots)):
        retList.append('break')

    return(retList)


def getListofTime(block):
    """
    Creates a list of time steps with a set duration. If the time blocks do not
    divide into the day evenly, the last item is a collection of the remainding
    time.

    block: length of each time block.
    return: list of time blocks.
    """
    day = 1440
    if day % block != 0:
        divisions = int(day/block)
        return numpy.linspace(0, block*(divisions), divisions+1)
        #raise ValueError('Please enter a time that can divide into {} evenly'.format(day))
    else:
        return numpy.linspace(0, day-block, day/block)

def getLongestBlock(itemList):
    """
    Sorts through a list of items (events that need to be scheduled) and finds
    longest time duration.

    itemList: list of events that need to be scheduled
    return: integer representing the number of seconds in the longest event
    """
    longestBlock = 15
    for event in itemList:
        if event.duration.total_seconds()/60 > longestBlock:
            longestBlock = event.duration.total_seconds()/60
    return longestBlock

#This function is used a temporary placeholder for the to-do list code
def getItemList(cal):
    """
    Reads a test calendar and creates a list of events
    """
    itemList = []
    for day in cal.days.values():
        for event in day.events:
            itemList.append(event)
    return itemList

def populateMatrix(timeList, taskList, matrix):
    """
    Parses through a cost-matrix and assigns each datapoint a unique
    value.

    timeList: Y-axis of matrix
    taskList: X-axis of matrix
    matrix: square matrix

    return: matrix with manipulated values
    """
    for y in range(len(taskList)):
        for x in range(len(timeList)):
            matrix[x][y] = random.randint(0,20)
    return matrix

def main(itemList):
    """
    Runs a set of steps to generate a cost matrix from a list of items.

    itemlist: list of events that need to be scheduled.
    """
    #below Segment of code for debugging purposes only
    tempFile = open('testData/willslife', 'rb')
    testCal = load(tempFile)
    testList = getItemList(testCal)
    del(testList[8])
    itemList = testList
    #above Segmenet for debugging purposes only

    #Need to add a for loop that iterates through all of the events
    timeBlock = getLongestBlock(itemList)
    timeList = getListofTime(timeBlock)
    taskList = getTaskList(timeList, testList)
    costMatrix = getCostMatrix(len(timeList))
    costMatrix = populateMatrix(timeList, taskList, costMatrix)
    print('list of time slots:', timeList)
    print('list of events:')
    for i in taskList:
        if i == 'break':
            print('break')
        else:
            print(i.name)
    print('cost matrix:', costMatrix)

    return costMatrix

if __name__ == "__main__":
    tempFile = open('testData/willslife', 'rb')
    testCal = load(tempFile)
    testList = getItemList(testCal)
    #del(testList[8])
    print(testList[8].duration.total_seconds()/60)
    #print(getListofTime(4000))
    # for i in testList:
        # print(i)
    matrix = main()
