''' Created by Jane Sieving (jsieving) on 4/14/18.
Loads a calendar file, prints it and saves it to a csv.'''

from schedule_helpers import *
from sys import argv
from pickle import dump, load

cal_name = argv[1]
loc = 'calendars/'
f = open(loc + cal_name, 'rb')
calendar = load(f)
calendar.print_days()
cal_to_csv(calendar)
