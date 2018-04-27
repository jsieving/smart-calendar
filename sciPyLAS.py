from scipy.optimize import linear_sum_assignment
import time, numpy, random
# import matrixManipulator
from scheduleHelpers import Item
from pickle import load, dump

def getCostMatrix(itemList, timeList):
    """
    Creates a  matrix.

    itemList: list of items with same duration
    timeLsit: list of time blocks

    return: matrix with dimensions len(IL)Xlen(TL)
    """
    matrix = []
    for row in range(len(itemList)):
        matrix.append([])
        for column in range(len(timeList)):
            matrix[row].append(100)
    return matrix


def getTaskList(timeBlock, itemList):
    """
    Creates a list of tasks that form the x-axis of the cost-matrix.

    itemList: list of items that need to be scheduled

    return: A list of items that have the same duration as the time block.
    """
    itemDuration = []
    retList = []
    for i in range(len(itemList)):
        itemDuration.append(itemList[i].duration.total_seconds()/60)

    for x in range(len(itemDuration)):
        if itemDuration[x] == timeBlock:
            retList.append(itemList[x])

    return retList


def getListofTime(block, offset):
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
    for day in cal.values():
        for event in day:
            itemList.append(event)
    return itemList

def populateMatrix(timeList, taskList, matrix):
    """
    Parses through a cost-matrix and assigns each datapoint a unique
    value.

    timeList: X-axis of matrix
    taskList: Y-axis of matrix
    matrix: any size

    return: matrix with manipulated values
    """
    for x in range(len(taskList)):
        for y in range(len(timeList)):
            matrix[x][y] = random.randint(0,20)
    return matrix

def runSorter():
  cost = [[2,2,5,1,2], [1,5,6,7,8], [5,5,5,5,4]]
  r_ind, c_ind = linear_sum_assignment(cost)
  print(r_ind, c_ind)


if __name__ == "__main__":
    tempFile = open('testData/willslife', 'rb')
    testCal  = load(tempFile)
    testList = getItemList(testCal)

    runSorter()


    # print(len(testList))
    #
    # while(len(testList) > 0):
    #     print(len(testList))
    #     longestBlock = getLongestBlock(testList)
    #     taskList = getTaskList(longestBlock, testList)
    #     timeList = getListofTime(longestBlock, 0)
    #     print('Task List=', taskList)
    #     print('Time List=', timeList)
    #
    #     matrix = getCostMatrix(taskList, timeList)
    #     print('matrix=', matrix)
    #
    #     retList = testList[:]
    #     print('length of retList=', len(retList))
    #     print('length of testList=', len(testList))import matrixManipulator
    #
    #     for i in testList:
    #         if i.duration.total_seconds()/60 == longestBlock:
    #             retList.remove(i)
    #     testList = retList[:]

    #print(getListofTime(4000))
    # for i in testList:
        # print(i)
#Dictionary of days, each day refers to a list of events
