from datetime import datetime
from gcal import GCal

def getListOfEvents(tempList):
    """
    This function returns a list of events that are not repeatable
    """
    retList = []
    for i in tempDict:
        if 'recurrence' not in i.keys():
            retList.append(i)
    return retList

def main():
    cal = GCal()

    events = cal.get_events()
    listOfItems = events['items']

    print(getListOfEventspr
    print(listOfItems[0])

if __name__ == "__main__":
    main()

'''
self, name, start = None, end = None, duration = None,\
            breakable = False, importance = None, category = None, item_type = 'event'):

This file stores on-demand the events that are in google calendar into a person's history.

This file should only store events that were created by the user or the alogrithm.

If the function tries to save the same event, it should spit an error
'''
