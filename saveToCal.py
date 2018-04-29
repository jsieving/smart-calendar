from datetime import datetime
from gcal import GCal
from scheduleHelpers import Item
import os
from pickle import load, dump

def getNonRepeatingEvents(tempList):
    """
    This function returns a list of events that are not repeatable.
    """
    retList = []
    for i in tempList:
        if 'recurrence' not in i.keys():
            retList.append(i)
    return retList

def getListOfItems(tempList):
    """
    Converts a list of google event objects to Item event objects.
    """
    retList = []
    for i in tempList:
        #assign google variables to local variables
        name = i['id']
        start= i['start']['dateTime']
        end= i['end']['dateTime']
        category= i['summary'].lower()

        #convert the string date into a dateTime object
        start= datetime(int(start[0:4]), int(start[5:7]),
                int(start[8:10]), int(start[11:13]), int(start[14:16]))
        end= datetime(int(end[0:4]), int(end[5:7]),
                int(end[8:10]), int(end[11:13]), int(end[14:16]))
        category= category.replace(" ", "")

        #save event as an item
        i = Item(name=name, start=start, end=end, category=category)
        retList.append(i)
    return retList

def storeListofItems():
    """
    Checks to see if user file system is present and, if not, will add
    a file system
    """
    directory = "userHistory"
    if not os.path.exists(directory):
        os.makedirs(directory)

    if len(os.listdir(directory)) > 0
        for filename in os.listdir(directory):
            print(filename)

def main():
    cal = GCal()
    events = cal.get_events(3, 1)
    tempList = events['items']
    print(tempList)
    tempList = getNonRepeatingEvents(tempList)
    tempList = getListOfItems(tempList)

    print(tempList)

    # print(getListOfEventspr)
    # print(listOfItems[0])

if __name__ == "__main__":
    storeListofItems()

'''
self, name, start = None, end = None, duration = None,
            breakable = False, importance = None, category = None, item_type = 'event'):

This file stores on-demand the events that are in google calendar into a person's history.

This file should only store events that were created by the user or the alogrithm.

If the function tries to save the same event, it should spit an error

datetime.datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
'''
