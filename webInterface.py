
from flask import Flask, render_template, redirect, url_for, request
from eventClass import Event
from gcal import GCal
app = Flask(__name__)


def generateEvent(name, date, startTime, endTime, breakable):
    submission = Event(name, date, startTime, endTime, breakable)
    print(submission)
    cal = GCal()
    cal.create_event(name=name, start=startTime )


#Defines what occurs when the webpage is opened
@app.route('/')
def index():
    return redirect(url_for('event'))

#Defines what occurs in the createEvent page
@app.route('/createEvent', methods=['GET', 'POST'])
#Function that runs when page opens
def event():
    if request.method == 'POST':
        #Finds status of checkbox
        if len(request.form) < 5:
            breakable = False
        else:
            breakable = True
        #Checks to see if all the boxes are filled
        if len(request.form['name']) < 1 or len(request.form['startTime']) < 1 or len(request.form['date'])< 1 or len(request.form['endTime'])<1:
            return redirect(url_for('index'))
        #Defines Variables
        name, date, startTime, endTime = (request.form['name'], request.form['date'],
                                                    request.form['startTime'],request.form['endTime'])
        generateEvent(name, date, startTime, endTime, breakable)
        return redirect(url_for('index'))
    #Defines what html page runs when page is opened
    return render_template('event.html')

if __name__ == '__main__':
    app.run()
