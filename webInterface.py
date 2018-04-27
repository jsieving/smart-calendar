
from flask import Flask, render_template, redirect, url_for, request
from scheduleHelpers import Item
#from toDo import make_list
from gcal import GCal
import datetime
import time

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
    #cal.create_event(name = name)
#Defines what occurs when the webpage is opened
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            request.form['event']==''
            return redirect("createEvent")
        except:
            print('works')
            return redirect("saveToCal")

    else:
        return render_template('index.html')

@app.route('/saveToCal')
def saveToCal():
    return render_template('saveToCal.html')
#Defines what occurs in the createEvent page
@app.route('/createEvent', methods=['GET', 'POST'])
#Function that runs when page opens
def event():
    if request.method == 'POST':
        #Finds status of checkbox
        if request.form['submit'] == 'submit':
            if len(request.form) < 4:
                breakable = False
            else:
                breakable = True
            #Checks to see if all the boxes are filled
            if len(request.form['name']) < 1 or len(request.form['startTime']) < 1 or len(request.form['endTime'])<1:
                return redirect(url_for('index'))
            #Defines Variables
            name, startTime, endTime= (request.form['name'],
                                        request.form['startTime'],request.form['endTime'])

            event = generateEvent(name, startTime, endTime)
            print(event)
            #make_list(event)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('saveToCal'))


    #Defines what html page runs when page is opened
    return render_template('event.html')

if __name__ == '__main__':
    cal = GCal()

    app.run()
