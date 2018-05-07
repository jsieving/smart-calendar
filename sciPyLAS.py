from scipy.optimize import linear_sum_assignment
import time, numpy, random
# import matrixManipulator
from scheduleHelpers import Item, csv_to_tasklist
from pickle import load, dump
from copy import copy, deepcopy
from preferenceScoring import *
from gcal import *

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

class LAS:
    '''A linear assignment solver which takes a list of events and finds the
    best way to schedule them.
    '''
    def __init__(self, itemList):
        self.initItemList = deepcopy(itemList) # Stores the original item list to run multiple iterations
        self.itemList = itemList # This copy gets modified with every iteration
        self.calendarSource = GCal()
        self.freq_costs = prefs_from_gcal(self.calendarSource)

    def getLongestBlock(self):
        """
        Sorts through a list of items (events that need to be scheduled) and finds
        longest time duration.

        itemList: list of events that need to be scheduled
        return: integer representing the number of seconds in the longest event
        """
        longestBlock = 15
        for event in self.itemList:
            if event.duration.total_seconds()/60 > longestBlock:
                longestBlock = event.duration.total_seconds()/60
        self.blockLength = longestBlock

    def getTaskList(self):
        """
        Creates a list of tasks that form the x-axis of the cost-matrix.

        itemList: list of items that need to be scheduled

        return: A list of items that have the same duration as the time block.
        """
        leftoverItems = []
        workingList = []
        for item in self.itemList:
            duration = item.duration.total_seconds()/60
            if duration == self.blockLength:
                workingList.append(item)
            else:
                leftoverItems.append(item)
        self.itemList = leftoverItems
        return workingList

    def makeCostDict(self):
        break_prefs = get_break_prefs(self.calendarSource)
        costs = get_timeblock_costs(self.blockLength, self.freq_costs, break_prefs)
        return costs

    def getTimeList(self, offset = 0):
        """
        Creates a list of time steps with a set duration. If the time blocks do not
        divide into the day evenly, the last item is a collection of the remaining
        time.

        blockLength: length of each time block.
        return: list of time blocks.
        """
        day = 1440
        if day % self.blockLength != 0:
            divisions = int(day/self.blockLength)
            self.timeList = numpy.linspace(0, self.blockLength*(divisions), divisions+1)
            #raise ValueError('Please enter a time that can divide into {} evenly'.format(day))
        else:
            self.timeList = numpy.linspace(0, day-self.blockLength, day/self.blockLength)

    def populateMatrix(self, itemList, costDict):
        """
        Parses through a cost-matrix and assigns each datapoint a unique
        value.

        timeList: X-axis of matrix
        taskList: Y-axis of matrix
        matrix: any size

        return: matrix with manipulated values
        """
        IL = len(itemList)
        TL = len(self.timeList)
        matrix = [[0 for i in range(TL)] for j in range(IL)]

        for x, item in enumerate(itemList):
            activity = item.category
            scores = costDict.get(activity, [0 for j in range(TL)])
            for y in range(TL):
                matrix[x][y] = scores[y]
        return matrix

    def run(self, matrix):
        return linear_sum_assignment(matrix)


if __name__ == "__main__":
    # tempFile = open('testData/willslife', 'rb')
    # testCal  = load(tempFile)
    # testList = getItemList(testCal)

    testList = csv_to_tasklist('toDoList')

    solver = LAS(testList)
    solver.getLongestBlock()
    solver.getTimeList()
    workingList = solver.getTaskList()
    costDict = solver.makeCostDict()
    costMatrix = solver.populateMatrix(workingList, costDict)
    results, results2 = solver.run(costMatrix)
    print(results)
    print(results2)

    # runSorter()
    #
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
    #     print('length of testList=', len(testList))
    #
    #     for i in testList:
    #         if i.duration.total_seconds()/60 == longestBlock:
    #             retList.remove(i)
    #     testList = retList[:]
    #
    # print(getListofTime(4000))
    # for i in testList:
    #     print(i)
# Dictionary of days, each day refers to a list of events
