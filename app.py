# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy


# create the application object
app = Flask(__name__)

# config
import os
#get configuration settings from config,py using enviroment variables
app.config.from_object(os.environ['APP_SETTINGS'])
# create the sqlalchemy object
db = SQLAlchemy(app)
# import db schema
from models import *

# method check login to prevent access to pages that require login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        #if logged in allow user to view page
        if 'logged_in' in session:
            return f(*args, **kwargs)
        #else redirect to the login page and prompt the user to login
        else:
            flash('You need to login first.')
            return redirect(url_for('welcome'))
    return wrap

# handel login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # if data has been entered
    if request.method == 'POST':
        # if user tries to login as administrator show invalid credentials
        if (request.form['username'] == 'admin') \
                or request.form['password'] == 'admin':
            error = 'Invalid Credentials. Please try again.'
        #allow user to login and create a session
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']

            return redirect(url_for('home'))
    #Show html page for login
    return render_template('login.html', error=error)



# controls interactions with messaging page
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #read all previously posted messages from database
    posts = db.session.query(MessagePost).all()
    #if a message is entered add it to the database and refresh page
    if request.method == 'POST':
        db.session.add(MessagePost(session['username'], request.form['message']))
        db.session.commit()
        return redirect(url_for('home'))
    #show html page form the main page
    return render_template('index.html', posts=posts)

#Create welcome page
@app.route('/welcome')
def welcome():
    return render_template('welcome.html') 

#Create logout transition
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()