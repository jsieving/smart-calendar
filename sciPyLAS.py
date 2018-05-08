from scipy.optimize import linear_sum_assignment
import numpy
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
        print('\nGetting break times...')
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
        day = 2880
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
        TL = len(self.timeList) - 1
        matrix = [[0 for i in range(TL)] for j in range(IL)]

        for x, item in enumerate(itemList):
            activity = item.category
            scores = costDict.get(activity, [0 for j in range(TL)])
            for y in range(TL):
                matrix[x][y] = scores[y]
        return matrix

    def run(self, matrix):
        return linear_sum_assignment(matrix)

    def postTempEvents(self, itemArray, timeArray, workingList):
        for n in range(len(itemArray)):
            item = workingList[itemArray[n]]
            time = self.timeList[timeArray[n]]
            item.start = min_to_dt(time, d = date(2018, 5, 8))
            item.end = item.start + item.duration
            print('Posted', item)
            self.calendarSource.create_event(name = item.name, start = item.start, end = item.end)



if __name__ == "__main__":
    # testList = csv_to_tasklist('toDoList')

    f = open('segmentedList', 'rb+')
    segList = load(f)

    solver = LAS(segList)
    solver.calendarSource.make_temp_cal()

    while solver.itemList:
        solver.getLongestBlock()
        solver.getTimeList()
        workingList = solver.getTaskList()
        costDict = solver.makeCostDict()
        costMatrix = solver.populateMatrix(workingList, costDict)
        itemArray, timeArray = solver.run(costMatrix)
        solver.postTempEvents(itemArray, timeArray, workingList)
