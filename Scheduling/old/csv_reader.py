import csv
from pickle import dump, load
from datetime import timedelta, datetime, date, time
from scheduling import *
from agenda_gen import min_to_dt

loc = 'calendars/'
cal_name = 'willslife'

csvfile = open('%s.csv' % cal_name)
data = csv.reader(csvfile)
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

cal.print_days()

f = open(loc + cal_name, 'wb+')
f.seek(0)
dump(cal, f)
f.close()
