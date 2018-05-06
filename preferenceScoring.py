'''Created by Jane Sieving (jsieving) on 4/20/18.'''

from scheduleHelpers import *
from gcal import *
from pickle import dump, load
from datetime import timedelta, datetime, date, time
import time
offset = time.gmtime().tm_hour - time.localtime().tm_hour

def prefs_from_csv(csv_name):
    '''Converts a csv file into a calendar, then creates a cost
    list from the contained events.'''
    csv_to_cal(csv_name)
    f = open('testData/' + csv_name, 'rb+')
    calendar = load(f)
    recurrence_list = []
    for day in calendar.values():
        for event in day:
            recurrence_list.append(event)
    prefs = get_freq_prefs(recurrence_list)
    return prefs

def prefs_from_gcal():
    events = get_events()['items']
    event_list = make_event_list(events)
    activities = extract_activities(event_list)
    activity_prefs = {}
    for activity, events in activities.items():
        activity_prefs[activity] = get_freq_prefs(events)

def get_freq_prefs(recurrence_list):
    '''Takes a list of events and returns a list representing the minutes of the
    week and the likelihood that an activity will occur in each minute.'''
    pref_list = []
    costs = []
    for j in range(int(1440 / 15)):
        pref_list.append(0)
        t = min_to_dt(j * 15)
        for e in recurrence_list:
            if e.start <= t <= e.end:
                pref_list[j] += 1
    for p in pref_list:
        c = int((1 - p/len(recurrence_list)) * 100)
        costs.append(c)
    return costs

def get_break_prefs(gcal):
    pref_list = []
    for i in range(24 *4):
        #this makes an array of costs for one day split by 15 minute increments
        pref_list.append(0)
    busy = gcal.get_busy()["calendars"][gcal.mainID]["busy"]
    for time in busy:
         start = datetime.strptime(time["start"], '%Y-%m-%dT%H:%M:%SZ')
         #this converts the start time to the index of the array, separated by 15 minute increments
         start = int(start.hour * 4 + start.minute / 15) - (offset * 4)
         end = datetime.strptime(time["end"], '%Y-%m-%dT%H:%M:%SZ')
         end = int(end.hour * 4 + end.minute / 15) - (offset * 4)
         for i in range(end - start):
             pref_list[start + i] = 100
    pref_list2 = []
    for i in range (len(pref_list) - 2):
        if(pref_list[i] == 100):
            pref_list2.append(1000)
        else:
            avg = (pref_list[i] + pref_list[i + 1] + pref_list[i + 2])/3
            pref_list2.append(avg)
    pref_list2.append(pref_list2[:-1])
    pref_list2.append(pref_list2[:-1])
    return pref_list2


def make_cost_matrix(cal, events):
    #soon this will multiply by history matrix
    event_list = []
    cost_matrix = []
    break_prefs = get_break_prefs(cal)
    for event in events:
        event_list.append(event.name)
        cost_matrix.append(get_break_prefs(cal))
    return event_list, cost_matrix
