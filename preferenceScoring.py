'''Created by Jane Sieving (jsieving) on 4/20/18.'''

from scheduleHelpers import min_to_dt
from datetime import timedelta, datetime, date, time

def get_time_preference(event_list):
    '''Takes a list of events and returns a list representing the minutes of the
    week and the likelihood that an activity will occur in each minute.'''
    pref_list = []
    costs = []
    for j in range(1440):
        pref_list.append(0)
        t = min_to_dt(j)
        for e in event_list:
            if e.start =< t =< e.end:
                pref_list[j] += 1
    for p in pref_list:
        c = int((1 - p/len(event_list)) * 100)
        costs.append(c)
