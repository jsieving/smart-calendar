'''Created by Jane Sieving (jsieving) on 4/20/18.'''

from scheduleHelpers import *
from pickle import dump, load
from datetime import timedelta, datetime, date, time

def prefs_from_csv(csv_name):
    '''Converts a csv file into a calendar, then creates a cost
    list from the contained events.'''
    csv_to_cal(csv_name)
    f = open('testData/' + csv_name, 'rb+')
    calendar = load(f)
    event_list = []
    for day in calendar.days.values():
        for event in day.events:
            event_list.append(event)
    prefs = get_time_prefs(event_list)
    return prefs

def get_time_prefs(event_list):
    '''Takes a list of events and returns a list representing the minutes of the
    week and the likelihood that an activity will occur in each minute.'''
    pref_list = []
    costs = []
    for j in range(1440):
        pref_list.append(0)
        t = min_to_dt(j)
        for e in event_list:
            if e.start <= t <= e.end:
                pref_list[j] += 1
    for p in pref_list:
        c = int((1 - p/len(event_list)) * 100)
        costs.append(c)
    return costs

print(prefs_from_csv('formula_events'))
