"""A simple "Hello, World" application using Flask."""

from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route('/createEvent', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run()
