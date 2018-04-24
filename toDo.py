import string
import pickle
from pickle import dump, load
from scheduleHelpers import Item

""" Import this .py into another .py, call the event_to_list function
Adds event object to a list and adds list to file
"""

loc = 'testData/'

my_event = Item('college')

if exists(loc + list_name):
    f = open(loc + list_name, 'rb+')
    todo_list = load(f)
else:
    f = open(loc + list_name, 'wb+')
    calendar = Calendar(cal_name)

def add_to_list(item):
    if exists(loc + list_name):
        f = open(loc + list_name, 'rb+')
        todo_list = load(f)
    else:
        f = open(loc + list_name, 'wb+')
        todo_list = []

    todo_list.append(item)
    f.seek(0)
    dump(todo_list, f)
    f.close()

make_list(my_event)
