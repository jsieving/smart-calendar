''' Created by Jane Sieving (jsieving) on 3/29/18.
Schedules the contents of a todo list into a calendar based on user's free time and other preferences. '''

from agenda_gen import *
from datetime import timedelta, datetime, date, time

class Item:
    '''An event created with or without scheduling information.
    name: str
    start, end: datetimes
    duration: time in minutes
    breakable: boolean
    due: datetime
    effort, importance: int 1-4
    category: string '''
    def __init__(self, name, start = None, end = None, duration = None,\
                importance = None, category = None):
        self.name = name
        self.start = start
        self.end = end
        self.duration = duration
        # self.breakable = breakable
        # self.due = due
        self.importance = importance
        self.category = category # may be replaced with tags?

    def __str__(self):
        return "\t%f | %s from %s to %s" % (self.preference, self.name, self.start.time(), self.end.time())

class Calendar:
    def __init__(self, name):
        self.name = name
        self.days = {}

class Day:
    def __init__(self, date):
        self.date = date
        self.events = []
        self.free_times = [(min_to_dt(0), min_to_dt(1439))]

    def print_events(self):
        print('Today is %s. You have %i events.' % (self.date, len(self.events)))
        for event in self.events:
            print(event)

def schedule_day(day, task_list):
    '''Given a day and a list of tasks, schedules as many of the events as will fit
    in the free time that day. '''
    free_times = day.free_times # List of available time slots in order of occurence
    while len(free_times) > 0 and len(todos) > 0: # While there's stuff to do and time to do it...
        time_slot = free_times[0]
        avail_time = time_slot[1]-time_slot[0] # Duration of the first available time slot
        fit_tasks = []
        for task in task_list: # Make a list of tasks that could be completed during this time
            if task.duration <= avail_time:
                fit_tasks.append(task)
        if len(fit_tasks) == 0: # If no tasks fit in this block, delete it from the queue and skip it
            del free_times[0]
            continue
        time_area = min_from_dt(time_slot[0])//480 # What part of the day it is, to determine user's work time preferences
        for task in fit_tasks: # Preference is a function of importance and other variables
            task.preference = task.importance  + effectiveness[task.category][time_area][0]# - hours_til_due/48 or something
        fit_tasks.sort(key=lambda r:r.preference) # sort tasks by preference
        fit_tasks[0].start = time_slot[0] # Assign the most preffered task to start in the current time slot
        fit_tasks[0].end = time_slot[0] + fit_tasks[0].duration # Assign end time

        if fit_tasks[0].duration + min_event_time >= avail_time: # If a task will consume a time block, delete it entirely
            del free_times[0]
        else:
            free_times[0] = (fit_tasks[0].end, time_slot[1]) # If there will be some time left over, make that the next time block
        day.events.append(fit_tasks[0]) # Since the task fits and is scheduled, add it to the day's events
        task_list.remove(fit_tasks[0]) # Remove it from the list of things to be scheduled

def add_item(name, duration, importance, category):
    '''Creates a basic unscheduled item and adds it to the todo list'''
    new_item = Item(name, duration = timedelta(minutes = duration), importance = importance, category = category)
    todos.append(new_item)

calendar = Calendar('My Calendar')
t = date(2004, 8, 9)
today = Day(t) # In practice, these would be initialized and stored in the calendar long ahead of time
calendar.days[t] = today

busy_times = random_timeblocks(8) # In practice, this would come from the events scheduled today
# print(busy_times)
today.free_times = busy_to_free(busy_times)
# print(today.free_times)

min_event_time = timedelta(minutes = 20) # This would be a user preference
todos = random_events(20, 120, 4) # Make a random to-do list for testing
'''
effectiveness: describes effectiveness/preference of working on 'task_type' during 'time_area'
values from -1:1, init at (0, 1) for (value, n of values). preference updater adds or subtracts a value
against the scaled running average to change it.
'''
effectiveness = {'QEA': [(.5, 1), (0, 1), (-.5, 1)], 'softdes': [(-.5, 1), (0, 1), (.5, 1)], \
                'eating': [(-.5, 1), (.5, 1), (-.5, 1)], 'nap': [(.5, 1), (0, 1), (.5, 1)]}


schedule_day(today, todos) # repeated event needs to be passed as a string composed of params
today.print_events()
