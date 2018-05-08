from scipy.optimize import linear_sum_assignment
import numpy
from scheduleHelpers import Item
from pickle import load, dump
from copy import copy, deepcopy
from preferenceScoring import *
from datetime import timedelta
from gcal import *

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
        return: integer representing the number of minutes in the longest event
        """
        longestBlock = 1
        for event in self.itemList:
            if event.duration > longestBlock:
                longestBlock = event.duration
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
            duration = item.duration
            if duration == self.blockLength:
                workingList.append(item)
            else:
                leftoverItems.append(item)
        self.itemList = leftoverItems
        return workingList

    def makeCostDict(self):
        """
        For the block length of the current batch of items, makes an <(activity: [costs])> dictionary
        where each cost is the sum of the preference costs and break costs for the entire time block.
        """
        break_prefs = get_break_prefs(self.calendarSource) # Recalculate busy/break times based on previously scheduled batch of events
        costs = get_timeblock_costs(self.blockLength, self.freq_costs, break_prefs)
        return costs

    def getTimeList(self, offset = 0):
        """
        Creates a list of time steps with a set duration. If the time blocks do not
        divide into the day evenly, the last item is a collection of the remaining
        time.

        The offset parameter allows costs to be calculated with events starting at different offsets.
        For example, offset = 0 tries scheduling events on the hour, offset = 30 tries scheduling events on the half hour.

        blockLength: length of each time block.
        return: list of time blocks.
        """
        minutes = 1440 * 7
        if minutes % self.blockLength != 0:
            divisions = int(minutes/self.blockLength)
            self.timeList = numpy.linspace(0, self.blockLength*(divisions), divisions+1)
        else:
            self.timeList = numpy.linspace(0, minutes-self.blockLength, minutes/self.blockLength)

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

    def runSolver(self, matrix):
        """
        Wrapper function a la ModSimPy. Runs the SciPy linear assignment solver on our event X timeslot matrix.
        """
        return linear_sum_assignment(matrix)

    def postTempEvents(self, itemArray, timeArray, workingList):
        """
        For each batch of events with the same duration, schedules events at the lowest-cost time according to the LAS results.
        Events are posted to the Temporary calendar.
        """
        for n in range(len(itemArray)):
            item = workingList[itemArray[n]]
            time = self.timeList[timeArray[n]]
            item.start = min_to_dt(time, d = date(2018, 5, 8))
            item.end = item.start + timedelta(minutes = item.duration)
            print('Posted', item)
            self.calendarSource.create_event(name = item.name, start = item.start, end = item.end)

def run():
    f = open('segmentedList', 'rb+') # Open the list of split-up todo items
    segList = load(f)
    f.close()

    solver = LAS(segList) # Initialize a solver with the list of events that need to get done

    while solver.itemList: # Repeat for each block length, while there are events to schedule
        print(solver.itemList)
        solver.getLongestBlock() # Find the longest event
        solver.getTimeList() # Split up the available time into slots the length of the longest event
        workingList = solver.getTaskList() # Find the items to be scheduled in this batch (the ones with the same length)
        costDict = solver.makeCostDict() # Sum up the costs for each activity for the time slots
        costMatrix = solver.populateMatrix(workingList, costDict) # populate a cost matrix for the events in the working list
        itemArray, timeArray = solver.runSolver(costMatrix) # Solve for which event should go in which time slot
        solver.postTempEvents(itemArray, timeArray, workingList) # Post this batch of events to the temporary calendar
