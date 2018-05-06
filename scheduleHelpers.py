'''Created by Jane Sieving (jsieving) on 4/10/18.
Contains class definitions and function definitions used for scheduling.'''

from csv import reader, writer
from pickle import dump, load
from datetime import timedelta, datetime, date, time

# __all__ = ["Item", "min_to_dt", "min_to_timedelta", "min_from_dt", "busy_to_free",
#             "cal_to_csv", "csv_to_cal", "partition", "add_item", "add_event", "event_to_gcal", "busy_from_gcal",
#             "categorize", "extract_activities"]
## Determines which functions are imported by 'import *'. If you add or change functions,
## make sure that is reflected here.

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
                breakable = False, importance = None, category = None, item_type = 'event',
                break_time = None, break_num = None):
        self.name = name
        self.start = start
        self.end = end
        self.duration = duration
        self.breakable = breakable
        # self.due = due
        self.importance = importance
        self.category = category # may be replaced with tags?
        self.item_type = item_type
        self.break_time = break_time
        self.break_num = break_num

    def __str__(self):
        return "%s from %s to %s" % (self.name, self.start.time(), self.end.time())

    def __repr__(self):
        return "%s from %s to %s" % (self.name, self.start.time(), self.end.time())

def create_dummy_events():
    events = []
    events.append(Item(name = "Party"))
    events.append(Item(name = "Linearity"))
    return events

class Category:
    """
    A class that is formatted to store a group of items within the same category
    filename: name of the pickled file
    tags: names that are associated with the category
    items: list of past items within the category
    """
    def __init__(self, filename, tags=None, items=None):
        self.filename= filename
        if tags == None:
            self.tags= []
        if items == None:
            self.items= []

    def __str__(self):
        return "acceptable names= {}\nitems= {}".format(self.tags, self.items)

    def addTag(self, newTag):
        self.tags.append(newTag)

    def addItem(self, newItem):
        self.items.append(newItem)

    def showStartTimes(self):
        retList = []
        for i in self.items:
            retList.append(i.start)
        return retList

    def showEndTimes(self):
        retList = []
        for i in self.items:
            retList.append(i.end)
        return retList

def min_to_dt(minutes, d = date(1, 1, 1)):
    '''Converts a number of minutes and a day to a time in that day, as a datetime object'''
    if minutes == 1440: # Prevents an issue when events end at midnight
        minutes -= 1
    hours, minutes = divmod(minutes, 60)
    t = time(hours, minutes)
    dt = datetime.combine(d, t)
    return dt

def min_to_timedelta(minutes):
    '''Converts a number of minutes to a timedelta object'''
    hours, minutes = divmod(minutes, 60)
    return timedelta(hours = hours, minutes = minutes)

def min_from_dt(dt):
    '''Converts a datetime to the number of minutes since the start of the day'''
    return dt.hour * 60 + dt.minute

def busy_to_free(busy_times):
    '''Takes a list of timeblocks in a day and returns the list timeblocks that are not
    included, for example given a list of busy times it will return all free times.
    It will work just as well to convert free to busy times.'''
    day = (min_to_dt(0), min_to_dt(1439))
    free_times = []
    for start, end in busy_times:
        time_span = day[0], start
        day = end, day[1]
        free_times.append(time_span)
    return free_times

def cal_to_csv(calendar):
    '''Takes a calendar object and creates a csv file of all the events in it'''
    loc = 'testData/'
    csvfile = open('%s%s.csv' % (loc, calendar.name), 'w')
    writer_ = writer(csvfile)
    headers = ['date', 'name', 'start', 'end', 'duration', 'breakable']
    writer_.writerow(headers)
    for date, day in calendar.days.items():
        for e in day.events:
            item = [date, e.name, e.start, e.end, e.duration, e.breakable]
            writer_.writerow(item)
    csvfile.close()

def csv_to_cal(cal_name):
    '''Takes a csv file formatted as a weekly log and creates a calendar object
    from it, then saves the calendar to a file.'''
    loc = 'testData/'
    csvfile = open('%s%s.csv' % (loc, cal_name))
    data = reader(csvfile)
    cal = {}
    for r, row in enumerate(data):
        if r == 0:
            continue
        Y, m, d = row[0].split('-')
        date_ = date(int(Y), int(m), int(d))
        name = row[1]
        start = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
        H, M, S = row[4].split(':')
        duration = timedelta(hours = int(H), minutes = int(M), seconds = int(S))
        if row[5] == 'True':
            breakable = True
        else:
            breakable = False
        item = Item(name, start, end, duration, breakable)
        if cal.get(date_):
            cal[date_].append(item)
        else:
            cal[date_] = [item]

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

def add_event(cal, name, start, end, duration, breakable, importance, category):
    '''Creates an event and adds it to the events for the given day'''
    item = Item(name, start, end, duration, breakable, importance, category)
    date_ = start.date()
    if cal.get(date_):
        cal[date_].append(item)
    else:
        cal[date_] = [item]

def categorize(event):
    '''Takes an Item and returns a string of what category it falls into.'''
    name = event.name.lower()
    a = "0123456789,.!?/()-'\""
    for char in a:
        name.replace(char, '')
    return name

def extract_activities(calendar_events):
    '''Takes a calendar or list of events and creates files for each activity.
    Each file is a pickled list of the events in that activity.
    Also returns a dictionary of activity lists.'''
    loc = 'testData/'
    if calendar_events.isinstance('dict'):
        all_events = []
        for date, day in calendar_events.items():
            for event in day:
                event.weekday = date.weekday()
                all_events.append(event)
    else:
        all_events = calendar_events
    activities = {}
    for event in all_events:
        act = categorize(event)
        if activities.get(act):
            activities[act].append(event)
        else:
            activities[act] = [event]
    for act, events in activities.items():
        f = open(loc + act, 'wb+')
        f.seek(0)
        dump(events, f)
        f.close()
    return activities

def item_from_gcal(event):
    '''Takes a GCal event (JSON format) and returns an object of our Item class.'''
    name = event['summary']
    start = event['start']['datetime'][0:-6]
    starttime = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
    end = event['end']['datetime'][0:-6]
    endtime = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
    item = Item(name = name, start = starttime, end = endtime)
    item.category = categorize(item)
    return item

def event_to_gcal(gcal, name, start, end):
    '''Pushes a simple event to Google Calendar'''
    gcal.create_event(name = name, start = start, end = end)

def busy_from_gcal(gcal, first_day, last_day):
    '''Gets all busy times within a range of days from Google Calendar, then
    returns a list of busy time blocks.'''
    busy_times = []
    time_min = datetime.combine(date = first_day, time = time(0, 0, 0))
    time_max = datetime.combine(date = last_day, time = time(23, 59, 0))
    response = gcal.get_busy(time_min, time_max)
    gcal_busy = response['calendars']['primary']['busy']
    for block in gcal_busy:
        start = block['start'][0:-6]
        starttime = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        end = block['end'][0:-6]
        endtime = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        busy_times.append((starttime, endtime))
    return busy_times
