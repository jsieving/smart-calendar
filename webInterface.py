from flask import Flask, render_template, redirect, url_for, request
from scheduleHelpers import Item
from toDo import make_list
from gcal import GCal
import datetime
import time
from saveToCal import saveToday
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

@app.route('/toDo')
def toDo():
    return render_template('toDo.html')

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
        make_list(event)
        return redirect(url_for('index'))


    #Defines what html page runs when page is opened
    return render_template('event.html')

if __name__ == '__main__':
    cal = GCal()

    app.run()
