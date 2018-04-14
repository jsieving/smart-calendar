''' Created by Jane Sieving (jsieving) on 4/10/18.
Runs an interactive program in the command line to allow the user to schedule events.'''

from os.path import exists
import parsedatetime as pdt
from datetime import timedelta, datetime, date, time
from pickle import dump, load
from gcal import GCal
from scheduleHelpers import *
from scheduler import schedule_day

loc = 'testData/'
parser = pdt.Calendar()

if __name__ == '__main__':
    gcal = GCal()

    eff = open(loc + 'effectiveness_data', 'rb+')
    effectiveness = load(eff)

    cal_name = input("Calendar name:\n>>> ")

    if exists(loc + cal_name): # Check if the calendar already exists and open it for editing
        print("Loading %s..." % cal_name)
        f = open(loc + cal_name, 'rb+')
        calendar = load(f)
    else:
        print("Creating new calendar %s..." % cal_name) # Create the new calendar and open it for editing
        f = open(loc + cal_name, 'wb+')
        calendar = Calendar(cal_name)

    now = datetime.now()
    today = date.today()
    d = input("Enter day to schedule events (hit Enter for today): ") # This section produces a date object to tag the calendar Day
    if d:
        day = parser.parseDT(d, now)[0].date() # Parse the text as a date
    else:
        day = today
    print(type(day))
    print(calendar.days.keys())
    if calendar.days.get(day): # Checks if the chosen day has already been defined
        curr_day = calendar.days[day] # If so, retrieves it from the calendar.
        curr_day.print_events()
    else:
        print("You have no schedule for this day.")
        curr_day = Day(day) # Creates a Day object for the chosen day
        calendar.days[day] = curr_day

    todos = []

    while True:
        response = input("Add new items to this calendar? (y/n)\n>>> ")
        if response[0].lower() == 'y':
            pass
        elif response[0].lower() == 'n':
            break
        name = input("Item name: ")
        st = input("Start time (if known): ")
        start = parser.parseDT(st, now)[0]
        end = input("End time (if known): ")
        end = parser.parseDT(end, now)[0]
        print(type(start), type(end))
        # dur = input("Duration (if known): ")
        # dur = parser.parseDT(dur, now)[0]
        # duration = dur - datetime.combine(today, time.min)
        # brk = input("Can this item be broken into shorter tasks? (y/n) ")
        # if response[0].lower() == 'y':
        #     breakable = True
        # elif response[0].lower() == 'n':
        #     breakable = False
        # importance = int(input("On a scale of 1-4, how important is this? "))
        # category = input("What category does this item go in? Enter '?' to list existing categories.\n>>> ")
        # if category == '?':
        #     print(effectiveness.keys())
        #     category = input("What category does this item go in? ")
        # if not effectiveness.get(category):
        #     effectiveness[category] = [(0, 1), (0, 1), (0, 1)]

        item = Item(name, start, end) #, duration, breakable, importance, category

        if start and end:
            item.duration = end - start
        elif start and duration:
            item.end = start + duration
        elif start:
            item.duration = default_duration
            item.end = start + duration
        else:
            item.item_type = 'todo'

        if item.item_type == 'todo':
            todos.append(item)
        else:
            curr_day.events.append(item)
            curr_day.update_freebusy(gcal)
            response3 = input("Add to Google Calendar? (y/n)\n>>> ")
            if response3[0].lower() == 'y':
                event_to_gcal(gcal, name, start, end)
            elif response3[0].lower() == 'n':
                pass

    response2 = input("Would you like me to schedule your tasks for you? (y/n)\n>>> ")
    if response2[0].lower() == 'y':
        schedule_day(curr_day, todos)
        curr_day.update_freebusy(gcal)
        curr_day.print_events()
    elif response2[0].lower() == 'n':
        pass

    cal_to_csv(calendar)

    f.seek(0)
    dump(calendar, f)
    f.close()

    eff.seek(0)
    dump(effectiveness, eff)
    eff.close()
