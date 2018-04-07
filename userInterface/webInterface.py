""" """

from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('event'))

@app.route('/createEvent', methods=['GET', 'POST'])
def event():
    error = None
    if request.method == 'POST':
        name, startTime, endTime = request.form['name'], request.form['startTime'], request.form['endTime']
        return redirect(url_for('index'))
    return render_template('event.html', error=error)

if __name__ == '__main__':
    app.run()
