
from flask import Flask, render_template, redirect, url_for, request
from item_class import Item
#import to_do.py
# from gcal import GCal
app = Flask(__name__)

# TODO fix how web html is parsed into python
# send that data to Google calendar

def generateEvent(name, startTime, endTime, date, breakable):
    submission = Item(name, startTime, endTime, date, breakable)
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
        if len(request.form) < 4:
            breakable = False
        else:
            breakable = True
        #Checks to see if all the boxes are filled
        if len(request.form['name']) < 1 or len(request.form['startTime']) < 1 or len(request.form['endTime'])<1 or len(request.form['date'])<1:
            return redirect(url_for('index'))
        #Defines Variables
        name, startTime, endTime, date = (request.form['name'],
                                                    request.form['startTime'],request.form['endTime'], request.form['date'])
        event = generateEvent(name, startTime, endTime, date, breakable)
        print(event)
        # event_to_list(event)

        return redirect(url_for('index'))
    #Defines what html page runs when page is opened
    return render_template('event.html')

if __name__ == '__main__':
    app.run()
