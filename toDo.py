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


FILE_LOCATION = "official_todo_list"
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
    if not os.path.exists(FILE_LOCATION):
        make_list()

    #Checks if item is valid (Handles people accidentally hitting submit button)
    if item == None:
        raise Exception("Invalid submission. Item:  {} \n Is not a valid item. Please resubmit".format(item))

    f = open(FILE_LOCATION, 'rb+')
    todo_list = load(f)
    todo_list.append(item)
    f.seek(0)
    dump(todo_list, f)
    f.close()

def make_list():
        """
        This function checks to see if there is a to-do list, create one, and will
        add events from google calendars.
        """
        #Check to see if the toDo file is present and add file if not
        fileLoc = "official_todo_list"
        if not os.path.exists(FILE_LOCATION):
            f = open(FILE_LOCATION, 'wb')
            todo_list = []
            dump(todo_list, f)
            f.close()

def get_list():
    f = open(FILE_LOCATION, "rb+")
    return pickle.load(f)

def clear_list():
    if not os.path.exists(FILE_LOCATION):
        make_list()
    f = open(FILE_LOCATION, "rb+")
    todo_list = load(f)
    print("opened in reading mode")
    todo_list.clear()
    print(todo_list)
    f.seek(0)
    dump(todo_list, f)
    f.close()
    print("deleted items from list")

def remove_from_list(name):
    todo_list = get_list()
    for item in range (len(todo_list)):
        if todo_list[item].name == name:
            print("cool!!!")
            todo_list.pop(item)
            print(todo_list)
    if os.path.exists(FILE_LOCATION):
        f = open(FILE_LOCATION, 'wb')
        f.seek(0)
        dump(todo_list, f)
        f.close()

if __name__ == "__main__":
    make_list(None)

# clear_list()
