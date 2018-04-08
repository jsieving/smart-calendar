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
        print('works_0')
        if request.form['breakable'] == '':
            breakable = True
        else:
            print('works_1')
            breakable = False
        if len(request.form['name'] < 1) or request.form['startTime'] < 1:
            return redirect(url_for('index'))
        name, startTime, endTime, breakable = request.form['name'], request.form['startTime'],request.form['endTime'], request.form['breakable']
        return redirect(url_for('index'))
    return render_template('event.html', error=error)

if __name__ == '__main__':
    app.run()
