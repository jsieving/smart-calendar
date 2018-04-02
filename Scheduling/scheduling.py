''' Created by Jane Sieving (jsieving) on 3/29/18.
Schedules the contents of a todo list into a calendar based on user's free time and other preferences. '''

from agenda_gen import *
from copy import copy
from datetime import timedelta, datetime, date, time
from pickle import dump, load
from os.path import exists
import parsedatetime as pdt

class Item:
    '''An event created with or without scheduling information.
    name: str
    start, end: datetimes
    duration: timedelta
    breakable: boolean
    due: datetime
    effort, importance: int 1-4
    category: string
    item_type: str 'todo' or 'event'
    '''
    def __init__(self, name, start = None, end = None, duration = None,\
                breakable = False, importance = None, category = None, item_type = 'event'):
        self.name = name
        self.start = start
        self.end = end
        self.duration = duration
        self.breakable = breakable
        # self.due = due
        self.importance = importance
        self.category = category # may be replaced with tags?
        self.item_type = item_type

    def __str__(self):
        return "%s from %s to %s" % (self.name, self.start.time(), self.end.time())

class Calendar:
    def __init__(self, name):
        self.name = name
        self.days = {}

    def print_days(self):
        for day in self.days.values():
            day.print_events()

class Day:
    def __init__(self, date):
        self.date = date
        self.events = []
        self.free_times = [(min_to_dt(0), min_to_dt(1439))]
        self.busy_times = []

    def print_events(self):
        print('Today is %s. You have %i events.' % (self.date, len(self.events)))
        for event in self.events:
            print(event)

def schedule_day(day, todo_list):
    '''Given a day and a list of tasks, schedules as many of the events as will fit
    in the free time that day. '''
    task_list = copy(todo_list) # Isolates task breaking to this scheduling iteration
    free_times = day.free_times # List of available time slots in order of occurence
    while len(free_times) > 0 and len(todos) > 0: # While there's stuff to do and time to do it...
        time_slot = free_times[0]
        avail_time = time_slot[1]-time_slot[0] # Duration of the first available time slot
        if avail_time < min_event_time: #If there's not enough free time to do anything, skip the block
            continue
        fit_tasks = []
        for task in task_list: # Make a list of tasks that could be completed during this time
            if task.duration <= avail_time:
                fit_tasks.append(task)
            elif task.breakable:
                fit_tasks.append(partition(task, avail_time))
        if len(fit_tasks) == 0: # If no tasks fit in this block, delete it from the queue and skip it
            del free_times[0]
            continue
        time_area = min_from_dt(time_slot[0])//480 # What part of the day it is, to determine user's work time preferences
        for task in fit_tasks: # Preference is a function of importance and other variables
            task.preference = task.importance  + effectiveness[task.category][time_area][0]# - hours_til_due/48 or something
        fit_tasks.sort(key=lambda r:r.preference) # sort tasks by preference
        fit_tasks[0].start = time_slot[0] # Assign the most preffered task to start in the current time slot
        if hasattr(fit_tasks[0], partial_time): # If this is a partial task, split it into two parts
            next_task = copy(fit_tasks[0])
            next_task.duration = next_task.partial_time
            remaining_task = copy(fit_tasks[0])
            remaining_task.duration -= partial_time
            task_list.replace(fit_tasks[0], remaining_task) # Shorten the task in the to-do list
        else:
            next_task = fit_tasks[0]
            task_list.remove(fit_tasks[0])
        next_task.end = next_task.start + next_task.duration # Assign end time

        if next_task.duration + min_event_time >= avail_time: # If a task will consume a time block, delete it entirely
            del free_times[0]
        else:
            free_times[0] = (next_task.end, time_slot[1]) # If there will be some time left over, make that the next time block
        day.events.append(next_task) # Since the task fits and is scheduled, add it to the day's events

def partition(task, avail_time):
    '''Takes a breakable task and a span of time and returns a portion of the task
    that will fit in the time.'''
    if task.duration / 2 < min_event_time: # If it can't be subdivided into 2 tasks, it doesn't fit.
        return None
    elif task.duration - avail_time < min_event_time:
        task.partial_time = task.duration - min_event_time
        return task
    else:
        task.partial_time = avail_time
        return task

def add_item(todos, name, duration, breakable, importance, category):
    '''Creates a basic unscheduled item and adds it to the todo list'''
    new_item = Item(name, duration, breakable, importance, category)
    todos.append(new_item)

def add_event(day, name, start, end, duration, breakable, importance, category):
    '''Creates an event and adds it to the events for the given day'''
    new_item = Item(name, start, end, duration, breakable, importance, category)
    day.events.append(new_item)

min_event_time = timedelta(minutes = 20) # This would be a user preference
default_duration = timedelta(minutes = 60)
loc = 'calendars/'
'''
effectiveness: describes effectiveness/preference of working on 'task_type' during 'time_area'
values from -1:1, init at (0, 1) for (value, n of values). preference updater adds or subtracts a value
against the scaled running average to change it.
'''

parser = pdt.Calendar()

if __name__ == '__main__':
    eff = open(loc + 'effectiveness_data', 'rb+')
    effectiveness = load(eff)

    cal_name = input("Calendar name:\n>>> ")

    if exists(loc + cal_name): # Check if the calendar already exists and open it for editing
        print("Loading %s..." % cal_name)
        f = open(loc + cal_name, 'rb+')
        calendar = load(f)
    else:
        print("Creating new calendar %s..." % cal_name) # Create the new calendar and open it for editing
        f = open(loc + cal_name, 'wb+')
        calendar = Calendar(cal_name)

    now = datetime.now()
    today = date.today()
    d = input("Enter day to schedule events (hit Enter for today): ") # This section produces a date object to tag the calendar Day
    if d:
        day = parser.parseDT(d, now)[0].date() # Parse the text as a date
    else:
        day = today
    print(type(day))
    print(calendar.days.keys())
    if calendar.days.get(day): # Checks if the chosen day has already been defined
        curr_day = calendar[day] # If so, retrieves it from the calendar.
        curr_day.print_events()
    else:
        print("You have no schedule for this day.")
        curr_day = Day(day) # Creates a Day object for the chosen day
        calendar.days[day] = curr_day

    todos = []

    while True:
        response = input("Add new items to this calendar? (y/n)\n>>> ")
        if response[0].lower() == 'y':
            pass
        elif response[0].lower() == 'n':
            break
        name = input("Item name: ")
        st = input("Start time (if known): ")
        start = parser.parseDT(st, now)[0]
        end = input("End time (if known): ")
        end = parser.parseDT(end, now)[0]
        dur = input("Duration (if known): ")
        dur = parser.parseDT(dur, now)[0]
        duration = dur - datetime.combine(today, time.min)
        brk = input("Can this item be broken into shorter tasks? (y/n) ")
        if response[0].lower() == 'y':
            breakable = True
        elif response[0].lower() == 'n':
            breakable = False
        importance = int(input("On a scale of 1-4, how important is this? "))
        category = input("What category does this item go in? Enter '?' to list existing categories.\n>>> ")
        if category == '?':
            print(effectiveness.keys())
            category = input("What category does this item go in? ")
        if not effectiveness.get(category):
            effectiveness[category] = [(0, 1), (0, 1), (0, 1)]

        item = Item(name, start, end, duration, breakable, importance, category)

        if start and end:
            item.duration = end - start
        elif start and duration:
            item.end = start + duration
        elif start:
            item.duration = default_duration
            item.end = start + duration
        else:
            item.item_type = 'todo'

        if item.item_type == 'todo':
            todos.append(item)
        else:
            curr_day.events.append(item)
            curr_day.busy_times.append((item.start, item.end))
            curr_day.free_times = busy_to_free(curr_day.busy_times)

    response2 = input("Would you like me to schedule your tasks for you? (y/n)\n>>> ")
    if response2[0].lower() == 'y':
        schedule_day(curr_day, todos)
        curr_day.print_events()
    elif response2[0].lower() == 'n':
        pass

    f.seek(0)
    dump(calendar, f)
    f.close()

    eff.seek(0)
    dump(effectiveness, eff)
    eff.close()
