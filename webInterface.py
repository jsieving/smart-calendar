from flask import Flask, render_template, redirect, url_for, request
from scheduleHelpers import Item
from toDo import add_item, get_list, remove_from_list
from gcal import GCal
import datetime
import time
from saveFromCal import saveToday
app = Flask(__name__)

# TODO fix how web html is parsed into python
# send that data to Google calendar

def generateEvent(name, startTime, endTime):

    submission = Item(name, startTime, endTime)
    #print(submission)
    # print(startTime)
    start = datetime.datetime.strptime(startTime, '%Y-%m-%dT%H:%M')
    end = datetime.datetime.strptime(endTime, '%Y-%m-%dT%H:%M')
    offset = time.gmtime().tm_hour - time.localtime().tm_hour
    start = start + datetime.timedelta(hours = offset)
    end = end + datetime.timedelta(hours = offset)
    cal.create_event(name=name, start= start, end = end)
    event = Item(name=name, start= start, end = end)
    # cal.create_event(name = name)
    return event

def generateToDo(name, hours, minutes, break_time):
    # length should be the total number of 15 minute segments
    # eventually, add the events to the to do list the appropriate num of
    # times for the breaks - e.g. 60 minute event in 30 minute segments
    # should make 2 events in to do lists
    hours_to_mins = int(hours) * 60 # convert hours to minutes
    length_mins = int(hours_to_mins) + int(minutes) # total num minutes

    # print('total minutes')
    # print(length_mins)

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
        # print('list of durations: ' + str(durs))

    else: # if duration not divisible by break size
        breakable = True
        remains = length_mins % break_time
        # print('remains: ' + str(remains))
        new_length_mins = int(length_mins - remains)
        # print('new_length_mins: ' + str(new_length_mins))
        break_num = int(new_length_mins / break_time)
        # print('break num: ' + str(break_num))
        for i in range(0, break_num):
            if i == 0:
                durs.append(break_time + remains)
            else:
                durs.append(break_time)
    # print('durations list: ' + str(durs))
    for i in range (0, break_num):
        event = Item(name=name, duration=durs[i], breakable=breakable, break_num=break_num)
        add_item(event)
    return event

#Renders an html doc for our home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#Saves today's schedule and renders a
#html doc
@app.route('/saveToCal')
def saveToCal():
    saveToday()
    return render_template('saveToCal.html')

@app.route('/toDo', methods=['GET', 'POST'])
def toDo():
    # print('HIIIII')
    elements = {'name': '', 'hours': '0', 'minutes': '0', 'breakSize': '0'}
    if request.method == 'POST':
        #Checks to see if all the boxes are filled
        # print(request.form['breakSize'])
        for i in elements:
            if request.form[i] != '':
                try:
                     elements[i] = int(request.form[i])
                except:
                     elements[i] = request.form[i]
        # print(elements.values())

        generateToDo(elements['name'], elements['hours'], elements['minutes'], elements['breakSize'])
    return render_template('toDo.html')

@app.route('/viewToDo', methods=['GET', 'POST'])
def viewToDo():
    print('list: ' + str(get_list()))
    elements = {}
    if request.method == 'POST':
        events = request.form
        for event in events:
            print('event: ', event)
            if (event != "submit"):
                remove_from_list(event, duration)
                print('deleted event: ' + str(event))
    #Deletes all checked

    return render_template('viewToDo2.html', todo_list = get_list())

@app.route('/viewCal', methods=['GET', 'POST'])
def viewCal():
    url = GCal().get_mainID()
    if request.method == 'GET':
        GCal().migrate_events()
    return render_template('viewCal.html', url = url)

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
        add_item(event)
        return redirect(url_for('index'))

    #Defines what html page runs when page is opened
    return render_template('event.html')

if __name__ == '__main__':
    cal = GCal()
    app.run()
