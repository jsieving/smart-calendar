import string
import pickle
from pickle import dump, load
from scheduleHelpers import Item
import os
from gcal import GCal
import saveFromCal

""" Call the make_list function to add an event object to a list and adds list to file
It also updates the gcal list every time it gets run
"""
# # for setup and testing purposes
# my_event = Item('hw')
# foo = []
# dump(foo, open("testData/listData", "wb"))
# print("tested")

# def make_list(item, cal_list)
def add_item(item):
    """
    This function adds an item to the to-do list.
    """
    #Check to see if the toDo file is present and add file if not
    fileLoc = "official_todo_list"
    if not os.path.exists(fileLoc):
        make_list()

    #Checks if item is valid (Handles people accidentally hitting submit button)
    if item == None:
        raise Exception("Invalid submission. Item:  {} \n Is not a valid item. Please resubmit".format(item))


# def make_list(item):
#         """
#         This function checks to see if there is a to-do list, create one, and will
#         add events from google calendars.
#         """
#         #Check to see if the toDo file is present and add file if not
#         fileLoc = "official_todo_list"
#         if not os.path.exists(fileLoc):
#             f = open(fileLoc, 'rb+')
#             todoList = []
#             dump(todo_List, f)
#             f.close()
#
#
#
#
#         #
#         cal_list = main()
#         f = open(fileLoc,  "rb+")
#         todo_list = load(f)
#         print("opened in reading mode")
#         # except (OSError, IOError) as e:
#         #     foo = item
#         #     dump(foo, open("testData/listData", "wb"))
#         #     print("threw exception")
    cal_list = main()
    try:
        f = open("testData/listData", "rb+")
        todo_list = pickle.load(f)
        print("opened in reading mode")
    except (OSError, IOError) as e:
        foo = item
        dump(foo, open("testData/listData", "wb"))
        print("threw exception")

    todo_list.append(item)
    f.seek(0)
    dump(todo_list, f)
    f.close()

    print("added to file")
    # # check for duplicate calendar events in saved list
    # # add new calendar events to todo_list
    # for i in range(0,len(cal_list)):
    #     add = True
    #     for j in range(0,len(todo_list)):
    #         if cal_list[i] == todo_list[j]:
    #             add = False
    #     if add == True:
    #         todo_list.append(cal_list[i])
    print(todo_list)

def get_list():
    f = open("testData/listData", "rb+")
    return pickle.load(f)
def clear_list():
    try:
        f = open("testData/listData", "rb+")
        todo_list = load(f)
        print("opened in reading mode")
    except (OSError, IOError) as e:
        foo = item
        dump(foo, open("testData/listData", "wb"))
        print("threw exception")
    todo_list.clear()
    print(todo_list)
    f.seek(0)
    dump(todo_list, f)
    f.close()
    print("deleted items from list")

if __name__ == "__main__":
    make_list(None)

# clear_list()
