import string
import pickle
from pickle import dump, load

""" Import this .py into another .py, call the event_to_list function
Adds event object to a list and adds list to file
"""

my_event = "Event"
my_list = ["stuff", "moreStuff"]

list_obj = open("testData/listData", "wb")
pickle.dump(my_list, list_obj)
list_obj.close()

def make_list(item):
    try:
            f = open("testData/listData", "rb+")
            foo = load(f)
            print("opened in reading mode")
    except (OSError, IOError) as e:
        foo = item
        dump(foo, open("testData/listData", "wb"))
        print("threw exception")

    foo.append('a')
    dump(foo, f)
    f.close()
    print("added to file")

make_list(my_event)
