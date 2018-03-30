''' Created by Jane Sieving (jsieving) on 3/29/18.
Provides helper functions for the scheduling algorithm, particularly to provide dummy data. '''

from random import sample, randint, choice

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
        return "\t%f | %s from %s to %s" % (self.preference, self.name, self.start, self.end)

categories = ['QEA', 'softdes', 'eating', 'nap']

def random_events(minimum, maximum, n):
    '''Returns a list of n randomly created events with duration between the min and max,
    no set time, a random importance and a random category. '''
    agenda = []
    for i in range(n):
        start = None
        end = None
        duration = randint(minimum, maximum)
        importance = randint(1, 5)
        category = choice(categories)
        name = category + ' ' + str(randint(0, 10))
        item = Item(name, start, end, duration, importance, category)
        agenda.append(item)
    return agenda

def random_timeblocks(n, blocklength = 15):
    '''Returns a list of n non-overlapping timeblocks, which are (start, end) tuples
    spanning a whole number of blocklengths. '''
    free_time = []
    blocks = range(0, 1440//blocklength)
    times = sample(blocks, 2*n)
    times.sort()
    for i in range(n):
        time_span = times.pop(0) * 15, times.pop(0) * 15
        free_time.append(time_span)
    return free_time

def busy_to_free(busy_time):
    '''Takes a list of timeblocks in a day and returns the list timeblocks that are not
    covered, for example given a list of busy times it will return all unused times. '''
    day = (0, 1440)
    free_time = []
    for start, end in busy_time:
        time_span = day[0], start
        day = end, day[1]
        free_time.append(time_span)
    return free_time
