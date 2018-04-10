import string

""" Takes input from user, puts it in a dictionary, adds dict to master list
Asks user for another event. If yes, adds new dict to list
"""

my_todo = []

go = True

while go:       # make a list of events from user input - change this to get input from web interface
    this_event = {} #temporary dictionary for a single event
    task = input("What activity would you like to schedule? ").lower()
    if task == '':
        this_event[''] = 1
    else:
        this_event[task] = 1

    start_t = input("When does the activity start? ").lower() #we can add more dictionary entries...
    if start_t == '':
        this_event[''] = 2
    else:
        this_event[start_t] = 2

    end_t = input("When does the activity end? ").lower()
    if end_t == '':
        this_event[''] = 3
    else:
        this_event[end_t] = 3

    my_todo.append(this_event)

    another = input("Would you like to add another task? y/n ").lower()
    if another == 'y':
        go = True
    elif another == 'n':
        break
print(my_todo)

todo = open('todo.txt', 'w+')
todo.write(str(my_todo)) # write to do list to file
