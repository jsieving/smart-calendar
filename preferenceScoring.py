'''Created by Jane Sieving (jsieving) on 4/20/18.'''

from scheduleHelpers import *
from gcal import *
from pickle import dump, load
from datetime import timedelta, datetime, date, time
from os.path import exists
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

def prefs_from_gcal(gcal):
    '''Gets events from GCal and returns a dictionary of preference vectors for each activity.'''
    events = gcal.get_events()['items']
    event_list = gcal.make_event_list(events)
    activities = extract_activities(event_list)
    occurence_data = get_occur_data(activities)
    freq_cost_vectors = get_freq_costs(occurence_data)
    return freq_cost_vectors

def get_occur_data(activities):
    '''Takes a dictionary of 'activity':[event_list] and saves a dictionary of occurence_data
    such as <('activity1': [0, 1, 2, 0], 'activity2': [0, 1, 1, 2])>
    '''
    if exists('testData/occurence_data'):
        f = open('testData/occurence_data', 'rb+')
        occur_data = load(f)
    else:
        f = open('testData/occurence_data', 'wb+')
        occur_data = {}

    for activity, event_list in activities.items():
        pref_list = occur_data.get(activity, [0 for i in range(1440//15 + 1)]) # the +1 is to store the total event count
        for j in range(int(1440 / 15)):
            t = min_to_dt(j * 15)
            for e in event_list:
                if e.start <= t <= e.end:
                    pref_list[j] += 1
            pref_list[-1] += len(event_list)
        occur_data[activity] = pref_list

    f.seek(0)
    dump(occur_data, f)
    return occur_data

def get_freq_costs(occurence_data):
    '''Takes a dictionary of occurences, subtracts a dictionary of when events have been rejected,
    and returns a dictionary of activity costs.'''
    if exists('testData/feedback_data'):
        f = open('testData/feedback_data', 'rb+')
        feedback_data = load(f)
    else:
        feedback_data = {}
    costs = {}
    for activity, occur_data in occurence_data.items():
        activity_costs = []
        for n in range(96):
            entry_count = occur_data[-1]
            feedback_list = feedback_data.get(activity, [0 for i in range(96)])
            score = occur_data[n] - feedback_list[n]
            c = int((1 - score/entry_count) * 100)
            activity_costs.append(c)
        costs[activity] = activity_costs
    return costs

def get_break_prefs(gcal):
    pref_list = [0 for n in range(96)]
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
    for i in range(len(pref_list) - 2):
        if(pref_list[i] == 100):
            pref_list2.append(1000)
        else:
            avg = (pref_list[i] + pref_list[i + 1] + pref_list[i + 2])/3
            pref_list2.append(avg)
    pref_list2.append(pref_list[-1]) # adds on last element of first list, since there's nothing to average
    pref_list2.append(pref_list[-1]) # again, since it averages over 3
    return pref_list2

def get_feedback_matrix(reject_events_list):
    ''' Takes a list of google event objects and creates/updates a matrix of user feedback.
    These values can be subtracted from the stored occurence data.'''
    if exists('testData/feedback_data'):
        f = open('testData/feedback_data', 'rb+')
        feedback_data = load(f)
    else:
        f = open('testData/feedback_data', 'wb+')
        feedback_data = {}

    for event in reject_events_list:
        item = item_from_gcal(event)
        activity = categorize(item)
        feedback_list = feedback_data.get(activity, [0 for i in range(1440//15)])
        for j in range(int(1440 / 15)):
            t = min_to_dt(j * 15)
            if item.start <= t <= item.end:
                feedback_list[j] += 1
        feedback_data[activity] = feedback_list

    f.seek(0)
    dump(feedback_data, f)
    return feedback_data

def get_timeblock_costs(block_length, freq_costs, break_prefs):
    '''Given a timeblock length, a dictionary of frequency costs, and a dictionary of break
    preferences, returns a dictionary of overall costs for intervals of the specified length.'''
    n = block_length // 15 # number of block costs to add together
    costs = {}
    for activity, cost_list in freq_costs.items():
        overall_costs = []
        for i in range(96):
            if i % n == 0: # every n blocks, the cost resets
                cost = 0
            cost += cost_list[i] + break_prefs[i] # the cost accumulates for n blocks
            if i+1 % n == 0: # if this is the last of a set of n blocks, append the cost
                overall_costs.append(cost)
        costs[activity] = overall_costs
    return costs


# def make_cost_matrix(cal, events):
#     #soon this will multiply by history matrix
#     event_list = []
#     cost_matrix = []
#     break_prefs = get_break_prefs(cal)
#     for event in events:
#         event_list.append(event.name)
#         cost_matrix.append(get_break_prefs(cal))
#     return event_list, cost_matrix
