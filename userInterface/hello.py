"""A simple "Hello, World" application using Flask."""

from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            print('attempted username=',request.form['username'])
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('login'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run()
