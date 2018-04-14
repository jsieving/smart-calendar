import string
from pickle import dump, load

""" Import this .py into another .py, call the event_to_list function
Adds event object to a list and adds list to file
"""

def make_list(to_do):
    fileObject = open(testData/toDo, 'wb')
    pickle.dump(fileObject, to_do)
