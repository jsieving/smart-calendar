''' Created by Jane Sieving (jsieving) on 3/29/18.
Provides helper functions for the scheduling algorithm, particularly to provide dummy data. '''

from random import sample, randint, choice
from datetime import timedelta, datetime, date, time
# from scheduling import Item

categories = ['QEA', 'softdes', 'eating', 'nap']

def min_to_dt(minutes, d = date(1, 1, 1)):
    if minutes == 1440:
        minutes -= 1
    hours, minutes = divmod(minutes, 60)
    t = time(hours, minutes)
    dt = datetime.combine(d, t)
    return dt

def min_to_timedelta(minutes):
    hours, minutes = divmod(minutes, 60)
    return timedelta(hours = hours, minutes = minutes)

def min_from_dt(dt):
    return dt.hour * 60 + dt.minute

# def random_events(minimum, maximum, n):
#     '''Returns a list of n randomly created events with duration between the min and max,
#     no set time, a random importance and a random category. '''
#     agenda = []
#     for i in range(n):
#         start = None
#         end = None
#         duration = min_to_timedelta(randint(minimum, maximum))
#         importance = randint(1, 5)
#         category = choice(categories)
#         name = category + ' ' + str(randint(0, 10))
#         item = Item(name, start, end, duration, importance, category)
#         agenda.append(item)
#     return agenda

def random_timeblocks(n, blocklength = 15):
    '''Returns a list of n non-overlapping timeblocks, which are (start, end) tuples
    spanning a whole number of blocklengths. '''
    free_times = []
    blocks = range(0, 1440//blocklength)
    times = sample(blocks, 2*n)
    times.sort()
    for i in range(n):
        start, end = times.pop(0) * blocklength, times.pop(0) * blocklength
        time_span = min_to_dt(start), min_to_dt(end)
        free_times.append(time_span)
    return free_times

def busy_to_free(busy_times):
    '''Takes a list of timeblocks in a day and returns the list timeblocks that are not
    covered, for example given a list of busy times it will return all unused times. '''
    day = (min_to_dt(0), min_to_dt(1439))
    free_times = []
    for start, end in busy_times:
        time_span = day[0], start
        day = end, day[1]
        free_times.append(time_span)
    return free_times
