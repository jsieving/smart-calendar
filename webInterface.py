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
    print(startTime)
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
    length_hours = hours * 4 # 15 minute segments worth of hours
    length_mins = (minutes) / 15 # 15 minute segments worth of minutes
    length = length_hours + length_mins # total num segments
    if break_time == 0:
        print('yes')
        breakable = False
        break_num = 0
    elif break_time > 0:
        breakable = True
        break_num = length / break_time
    event = Item(name=name, duration=length, breakable=breakable, break_time=break_time, break_num=break_num)
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
    print('HIIIII')
    elements = {'name': '', 'hours': '0', 'minutes': '0', 'breakSize': '0'}
    if request.method == 'POST':
        #Checks to see if all the boxes are filled
        print(request.form['breakSize'])
        for i in elements:
            if request.form[i] != '':
                try:
                     elements[i] = int(request.form[i])
                except:
                     elements[i] = request.form[i]
        print(elements.values())

        generateToDo(elements['name'], elements['hours'], elements['minutes'], elements['breakSize'])
    return render_template('toDo.html')

@app.route('/viewToDo', methods=['GET', 'POST'])
def viewToDo():
    print(get_list())
    elements = {}
    if request.method == 'POST':
        events = request.form
        print(events)
        for event in events:
            if (event != "submit"):
                remove_from_list(event)
                print(event)
    #Deletes all checked


    return render_template('viewToDo2.html', todo_list = get_list())

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
