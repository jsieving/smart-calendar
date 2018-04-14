import string
from pickle import dump, load

""" Import this .py into another .py, call the event_to_list function
Adds event object to a list and adds list to file
"""

def make_todo(todo_list)
    my_todo = []
    fileObject = open(file_name, 'wb')
    pickle.dump(fileObject, my_todo)

    todo = open('todo.txt', 'w+')
    todo.write(str(my_todo)) # write to do list to file

    def event_to_list(event):
        my_todo.append(event)
        todo = open('todo.txt', 'w+')
        todo.write(str(my_todo)) # write to do list to file
        return todo
