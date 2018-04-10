'''Created by Jane Sieving (jsieving) on 4/10/18.
Contains class definitions and function definitions used for scheduling.'''

from csv import reader, writer
from pickle import dump, load
from random import sample, randint, choice
from datetime import timedelta, datetime, date, time
#import GCal as gc

class Item:
    '''An event created with or without scheduling information.
    name: str
    start, end: datetimes
    duration: timedelta
    breakable: boolean
    due: datetime (TBD)
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

    def update_freebusy(self, include_events = True):
        self.busy_times = busy_from_gcal(self.date, self.date)
        if include_events:
            for block in self.events:
                self.busy_times.append((block.start, block.end))
        self.busy_times.sort()
        self.free_times = busy_to_free(self.busy_times)

    def print_events(self):
        print('Today is %s. You have %i events.' % (self.date, len(self.events)))
        for event in self.events:
            print(event)

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

def cal_to_csv(calendar):
    csvfile = open('%s.csv' % calendar.name, 'w')
    writer = writer(csvfile)
    headers = ['date', 'name', 'start', 'end', 'duration', 'breakable']
    writer.writerow(headers)
    for date, e in calendar.days.items():
        item = [date, e.name, e.start, e.end, e.duration, e.breakable]
    csvfile.close()

def csv_to_cal(cal_name):
    csvfile = open('%s.csv' % cal_name)
    data = reader(csvfile)
    width = 8
    curr_activity = None
    downtime = ['sleep', 'transition', 'break']
    cal = Calendar(cal_name)
    for i in range(1, width):
        for r, row in enumerate(data):
            if r == 0:
                header = row[i].split('/')
                date = date(int(header[2]), int(header[0]), int(header[1]))
                day = Day(date)
                cal.days[date] = day
            else:
                start = min_to_dt(int(row[0]))
                end = min_to_dt(int(row[0]) + 15)
                duration = timedelta(minutes = 15)
                if row[i] in downtime:
                    continue
                if row[i] == curr_activity:
                    curr_item.end = end
                    curr_item.duration += duration
                else:
                    curr_activity = row[i]
                    name = row[i]
                    curr_item = Item(name, start, end, duration)
                    day.events.append(curr_item)
    loc = 'calendars/'
    f = open(loc + cal_name, 'wb+')
    f.seek(0)
    dump(cal, f)
    f.close()

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

def event_to_gcal(gcal, name, start, end):
    gcal.create_event(name = name, start = start, end = end)

def busy_from_gcal(first_day, last_day):
    busy_times = []
    time_min = datetime(date = first_day, time = time(0, 0, 0))
    time_max = datetime(date = last_day, time = time(23, 59, 0))
    response = gc.get_busy(time_min, time_max)
    gcal_busy = response['calendars']['primary']['busy']
    for block in gcal_busy:
        start = block['start'][0:-6]
        starttime = strptime(start, '%Y-%m-%dT%H:%M:%S')
        end = block['end'] # [0:-6]
        endtime = strptime(end, '%Y-%m-%dT%H:%M:%S')
        busy_times.append((starttime, endtime))
    return busy_times
