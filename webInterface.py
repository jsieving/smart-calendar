from flask import Flask, render_template, redirect, url_for, request
from scheduleHelpers import Item
from toDo import add_item, get_list, remove_from_list, make_list
from gcal import GCal
import datetime
import time
import sciPyLAS
app = Flask(__name__)

# TODO fix how web html is parsed into python
# send that data to Google calendar

def generateEvent(name, startTime, endTime):

    submission = Item(name, startTime, endTime)
    start = datetime.datetime.strptime(startTime, '%Y-%m-%dT%H:%M')
    end = datetime.datetime.strptime(endTime, '%Y-%m-%dT%H:%M')
    offset = time.gmtime().tm_hour - time.localtime().tm_hour
    start = start + datetime.timedelta(hours = offset)
    end = end + datetime.timedelta(hours = offset)
    cal.create_event(name=name, start= start, end = end, calendar = 'main')
    event = Item(name=name, start= start, end = end)
    return event

def segmentEvent(event):
    name = event.name
    length_mins = event.duration
    break_time = event.break_time
    durs = []

    if break_time == 0 or length_mins - break_time < 0: # case where not breakable
        # print('no breaks')
        breakable = False
        break_num = 1
        durs.append(length_mins)

    elif (length_mins) % break_time == 0: # if duration is divisible by break size
        breakable = True
        break_num = int(length_mins / break_time)
        # print('break_num: ' + str(break_num))
        for i in range(0, break_num):
            durs.append(break_time)

    else: # if duration not divisible by break size
        breakable = True
        remains = length_mins % break_time
        new_length_mins = int(length_mins - remains)
        break_num = int(new_length_mins / break_time)
        for i in range(0, break_num):
            if i == 0:
                durs.append(break_time + remains)
            else:
                durs.append(break_time)

    make_list('segmentedList')
    for i in range (0, break_num):
        event = Item(name=name, duration=durs[i], breakable=breakable, break_num=break_num)
        add_item(event, 'segmentedList')

def generateToDo(name, hours, minutes, break_time):
    length_hours = hours * 4 # 15 minute segments worth of hours
    length_mins = int(minutes) / 15 # 15 minute segments worth of minutes
    length = length_hours + length_mins # total num segments
    print('Length:', length)
    if break_time == 0:
        print('yes')
        breakable = False
        break_num = 0
    elif break_time > 0:
        breakable = True
        break_num = length / break_time
    event = Item(name=name, duration=length, breakable=breakable, break_time=break_time, break_num=break_num)
    add_item(event)
    segmentEvent(event)
    return event

#Renders an html doc for our home page
@app.route('/', methods=['GET', 'POST'])
def index():
    #GCal().migrate_events()
    make_list()
    return render_template('index.html')

@app.route('/toDo', methods=['GET', 'POST'])
def toDo():
    # print('HIIIII')
    elements = {'name': '', 'hours': '0', 'minutes': '0', 'breakSize': '0'}
    if request.method == 'POST':
        #Checks to see if all the boxes are filled
        for i in elements:
            if request.form[i] != '':
                try:
                     elements[i] = int(request.form[i])
                except:
                     elements[i] = request.form[i]

        generateToDo(elements['name'], elements['hours'], elements['minutes'], elements['breakSize'])
    return render_template('toDo.html')

@app.route('/viewToDo', methods=['GET', 'POST'])
def viewToDo():
    elements = {}
    if request.method == 'POST':
        events = request.form
        print('events: ', events)
        for event in events:
            thing = event
            duration = request.form[thing]
            print('request form: ', request.form[thing])
            print('event: ', event)
            if (event != "submit"):
                remove_from_list(event, duration)
    #Deletes all checked
    todo_list = get_list()
    print(todo_list)
    # for item in todo_list:
    #     print(item.duration)
    #     item.duration *= 15

    return render_template('viewToDo2.html', todo_list = todo_list)

@app.route('/viewCal', methods=['GET', 'POST'])
def viewCal():
    gcal = GCal()
    id1 = gcal.get_tempID()
    oldEvents = gcal.get_events(calendar = 'temp', daysPast = 2, daysFuture = 7)
    gcal.delete_multiple('main', oldEvents)
    if request.method == 'GET':
        sciPyLAS.run()
        tempList = gcal.get_events(calendar = 'temp', daysPast = 0, daysFuture = 7)
    if request.method == 'POST':
        gcal.migrate_events()
        print(request.form)
        for i in tempList:
            ID = i.name
            try:
                temp = request.form[ID]
                print('deleting')
                gcal.delete_event('temp',ID)
            except:
                pass

    return render_template('viewCal.html', id1 = id1, tempList=tempList)

@app.route('/createEvent', methods=['GET', 'POST'])
#Function that runs when page opens
def event():
    elements = {'name': '', 'startTime': '0', 'endTime': '0'}
    print('works', elements['name'])
    if request.method == 'POST':
        #Checks to see if all the boxes are filled
        for i in elements:
            if request.form[i] != '':
                elements[i] = request.form[i]

        print(elements.values())
        event = generateEvent(elements['name'], elements['startTime'], elements['endTime'])
        print(event)
        return redirect(url_for('index'))

    #Defines what html page runs when page is opened
    return render_template('event.html')

if __name__ == '__main__':
    cal = GCal()
    app.run()
