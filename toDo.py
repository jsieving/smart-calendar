import string
import pickle
from pickle import dump, load
from scheduleHelpers import Item

""" Import this .py into another .py, call the event_to_list function
Adds event object to a list and adds list to file
"""

my_event = Item('math')
# my_list = []
# my_list.append(my_event)
# print(my_list)

# my_list = []
# list_obj = open("testData/listData", "wb")
# pickle.dump(my_list, list_obj)
# list_obj.close()

def make_list(item):
    try:
        f = open("testData/listData", "rb+")
        foo = load(f)
        print(foo)
        print("opened in reading mode")
    except (OSError, IOError) as e:
        foo = item
        dump(foo, open("testData/listData", "wb"))
        print("threw exception")

    foo.append(item)
    print(foo)
    dump(foo, f)
    f.close()
    print("added to file")
    f = open("testData/listData", "rb+")
    foo2 = load(f)
    print(foo2)
    f.close()

make_list(my_event)
list_obj = open("testData/listData", "r")
print(list_obj)
