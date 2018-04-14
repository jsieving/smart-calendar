''' Created by Jane Sieving (jsieving) on 4/10/18.
Schedules the contents of a todo list into a calendar based on user's free time and other preferences. '''

from copy import copy
from os.path import exists

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
