from datetime import datetime
from gcal import GCal
from scheduleHelpers import Item, Category
import os
from pickle import load, dump

def getNonRepeatingEvents(daysPast, daysFuture):
    """
    This function returns a list of events that are not repeatable.
    """
    tempList = getListOfItems(daysPast, daysFuture)
    retList = []
    for i in tempList:
        if 'recurrence' not in i.keys():
            retList.append(i)
    return retList

def getListOfItems(daysPast, daysFuture):
    """
    Converts a list of google event objects to Item event objects.
    """
    cal = GCal()
    events = cal.get_events(daysPast,daysFuture)
    tempList = events['items']
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

def storeListOfItems(itemList):
    """
    This function takes a list of items and stores them in the user's history.
    If the file already exists, it is skipped.
    """
    directory = "userHistory"
    if not os.path.exists(directory):
        os.makedirs(directory)

    for item in itemList:
        exists = False
        itemTag = item.category

        #Runs through files in user history to find a category that matches
        #the item category
        for filename in os.listdir(directory):
            loc = directory + '/' + filename
            f = open(loc, "rb+")
            category = load(f)

            #Runs through items within a category and adds the new item if
            #there are no duplicate items found.
            if itemTag == category.filename:
                written = False
                exists = True
                for i in category.items:
                    if i.name == item.name:
                        written = True
                if not written:
                    category.addItem(item)
                    f.seek(0)
                    dump(category, f)
                    f.close()
                    break
                f.close()

        #Creates a new category file if there is no category that matches the
        #category of the new item.
        if not exists:
            newCategory = Category(filename=itemTag)
            newCategory.addTag(itemTag)
            newCategory.addItem(item)
            f = open(directory + "/" + itemTag, "wb")
            dump(newCategory, f)
            f.close()

def saveToday():
    """
    Saves a list of google events in today's schedule
    """
    tempList = getNonRepeatingEvents(1, 0)

    return temp

def readHistory():
    """
    This function shows all of the saved lists within
    userHistory for debugging purposes.
    """
    directory = 'userHistory'
    for filename in os.listdir(directory):
        loc = directory + '/' + filename
        f = open(loc, "rb+")
        f.seek(0)
        category = load(f)
        print(category)
        f.close()

def main(daysPast, daysFuture):
    """
    This functions runs a set of commands for debugging
    purposes.
    """
    tempList = getNonRepeatingEvents(daysPast, daysFuture)
    storeListOfItems(tempList)

    # print(getListOfEventspr)
    # print(listOfItems[0])

if __name__ == "__main__":
    main(1, 0)
    readHistory()
