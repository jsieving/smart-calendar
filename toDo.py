import string
import pickle
from pickle import dump, load
from scheduleHelpers import Item
import os
from gcal import GCal

""" Import this .py into another .py, call the event_to_list function
Adds event object to a list and adds list to file
"""

# my_event = Item('hw')
# foo = []
# dump(foo, open("testData/listData", "wb"))
# print("tested")

def make_list(item):
    try:
        f = open("testData/listData", "rb+")
        todo_list = load(f)
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

    f.close()
